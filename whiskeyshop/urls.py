from django.urls import path
from .views import HomePageView
from . import views

app_name = 'whiskeyshop'

app_name = 'whiskeyshop'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('whiskeys/', views.whiskey_list, name='whiskey_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:whiskey_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
]
