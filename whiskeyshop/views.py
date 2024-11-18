from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Whiskey, Cart, CartItem
from django.contrib.auth.decorators import login_required

# View to display all available whiskey
def whiskey_list(request):
    whiskeys = Whiskey.objects.all()
    return render(request, 'whiskeyshop/whiskey_list.html', {'whiskeys': whiskeys})

# View to show the user's cart
@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user, is_active=True)
    return render(request, 'whiskeyshop/cart.html', {'cart': cart})

# Add an item to the cart
@login_required
def add_to_cart(request, whiskey_id):
    whiskey = Whiskey.objects.get(id=whiskey_id)
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, whiskey=whiskey)

    # Increment quantity if the item already exists in the cart
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('whiskeyshop:view_cart')

# Remove an item from the cart
@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('whiskeyshop:view_cart')

# Empty the cart
@login_required
def empty_cart(request):
    cart = Cart.objects.get(user=request.user, is_active=True)
    cart.items.all().delete()
    return redirect('whiskeyshop:view_cart')


class HomePageView(TemplateView):
    template_name = 'home.html'
    
