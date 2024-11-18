from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import whiskeyshop
from .cart import Cart

def cart_add(request, whiskey_id):
    cart = Cart(request)
    whiskey = get_object_or_404(Whiskey, id=whiskey_id)
    cart.add(whiskey=whiskey, quantity=1)
    return redirect('cart_detail')

def cart_remove(request, whiskey_id):
    cart = Cart(request)
    whiskey = get_object_or_404(Whiskey, id=whiskey_id)
    cart.remove(whiskey)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

def whiskey_list(request):
    whiskeys = Whiskey.objects.all()  # Fetch all whiskey products
    return render(request, 'store/whiskey_list.html', {'whiskeys': whiskeys})


class HomePageView(TemplateView):
    template_name = 'home.html'
    
