from django.urls import path
from .views import HomePageView

urlpatterns = [
    path('cart/add/<int:whiskey_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:whiskey_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('', HomePageView.as_view(), name='home'),
    path('whiskeys/', views.whiskey_list, name='whiskey_list'),
]
