from django.urls import path
from .views import WhiskeyPageView

app_name = 'whiskeycellar'

urlpatterns = [
    path('jameson/', WhiskeyPageView.as_view(), name='jameson'),
]
