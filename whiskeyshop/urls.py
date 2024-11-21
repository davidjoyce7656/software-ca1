from django.urls import path
from .views import HomePageView
from . import views

app_name = 'whiskeyshop'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]