from django.shortcuts import redirect, render, get_object_or_404
from whiskeycellar.models import Whiskey
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
from order.models import Order, OrderItem
from django.urls import reverse
from stripe.error import StripeError
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Cart-related views
def add_cart(request, product_id):
    product = Whiskey.objects.get(id=product_id)
    cart = _get_or_create_cart(request)
    _add_or_update_cart_item(cart, product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    total, counter, discount, new_total, voucher = _calculate_cart_details(request)
    cart_items = _get_cart_items(request)
    stripe_total = _calculate_stripe_total(total, discount)

    if request.method == 'POST':
        return _handle_stripe_checkout(request, stripe_total, total, voucher)

    voucher_apply_form = VoucherApplyForm()
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'voucher_apply_form': voucher_apply_form,
        'new_total': new_total,
        'voucher': voucher,
        'discount': discount
    })


def cart_remove(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Whiskey, id=product_id)
    _remove_cart_item(cart, product)
    return redirect('cart:cart_detail')


def full_remove(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Whiskey, id=product_id)
    _delete_cart_item(cart, product)
    return redirect('cart:cart_detail')


def empty_cart(request):
    cart = _get_cart(request)
    if cart:
        CartItem.objects.filter(cart=cart, active=True).delete()
        cart.delete()
    return redirect('whiskeycellar:all_whiskeys')


# Helper methods for cart
def _get_or_create_cart(request):
    try:
        return Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        return cart


def _add_or_update_cart_item(cart, product):
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, cart=cart)


def _get_cart(request):
    try:
        return Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        return None


def _remove_cart_item(cart, product):
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass


def _delete_cart_item(cart, product):
    try:
        CartItem.objects.get(product=product, cart=cart).delete()
    except CartItem.DoesNotExist:
        pass


def _calculate_cart_details(request):
    total, counter = 0, 0
    discount, new_total = 0, 0
    voucher = None
    cart_items = _get_cart_items(request)

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        counter += cart_item.quantity

    voucher_id = request.session.get('voucher_id')
    if voucher_id:
        try:
            voucher = Voucher.objects.get(id=voucher_id)
            discount = total * (voucher.discount / Decimal('100'))
            new_total = total - discount
        except Voucher.DoesNotExist:
            pass

    return total, counter, discount, new_total, voucher


def _get_cart_items(request):
    cart = _get_cart(request)
    if cart:
        return CartItem.objects.filter(cart=cart, active=True)
    return []


def _calculate_stripe_total(total, discount):
    if discount:
        return int((total - discount) * 100)
    return int(total * 100)


def _handle_stripe_checkout(request, stripe_total, total, voucher):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Order from Perfect Cushion Shop'},
                    'unit_amount': stripe_total,
                },
                'quantity': 1,
            }],
            mode='payment',
            billing_address_collection='required',
            success_url=request.build_absolute_uri(
                reverse('cart:new_order', args=[voucher.id])
            ) + f"?session_id={{CHECKOUT_SESSION_ID}}&voucher_id={voucher.id}&cart_total={total}",
            cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        cart_items = _get_cart_items(request)
        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total': total,
            'error': str(e),
        })


# Order-related views
def create_order(request, voucher_id):
    try:
        session_id = request.GET.get('session_id')
        cart_total = request.GET.get('cart_total')

        session = _retrieve_stripe_session(session_id)
        customer_details = session.customer_details
        order_details = _create_order_from_session(session, customer_details)

        cart_items = _get_cart_items(request)
        _process_order_items(cart_items, order_details, cart_total, voucher_id)
        empty_cart(request)

        return redirect('order:thanks', order_details.id)

    except Exception as e:
        print(f"Error: {e}")
        return redirect("whiskeycellar:all_whiskeys")


def _retrieve_stripe_session(session_id):
    if not session_id:
        raise ValueError("Session ID not found.")
    return stripe.checkout.Session.retrieve(session_id)


def _create_order_from_session(session, customer_details):
    address = customer_details.address
    return Order.objects.create(
        token=session.id,
        total=session.amount_total / 100,
        emailAddress=customer_details.email,
        billingName=customer_details.name,
        billingAddress1=address.line1,
        billingCity=address.city,
        billingPostcode=address.postal_code,
        billingCountry=address.country,
        shippingName=customer_details.name,
        shippingAddress1=address.line1,
        shippingCity=address.city,
        shippingPostcode=address.postal_code,
        shippingCountry=address.country,
    )


def _process_order_items(cart_items, order_details, cart_total, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    for item in cart_items:
        _create_order_item(item, order_details, voucher)
    order_details.voucher = voucher
    order_details.discount = Decimal(cart_total) * (voucher.discount / Decimal('100'))
    order_details.total = Decimal(cart_total) - order_details.discount
    order_details.save()


def _create_order_item(cart_item, order_details, voucher):
    order_item = OrderItem.objects.create(
        product=cart_item.product.name,
        quantity=cart_item.quantity,
        price=cart_item.product.price,
        order=order_details
    )
    _update_product_stock(cart_item)
    _apply_voucher_discount(order_item, voucher)
    order_item.save()


def _update_product_stock(cart_item):
    product = cart_item.product
    product.stock -= cart_item.quantity
    product.save()


def _apply_voucher_discount(order_item, voucher):
    if voucher:
        discount = order_item.price * (voucher.discount / Decimal('100'))
        order_item.price -= discount






