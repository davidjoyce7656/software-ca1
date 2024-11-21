from django.urls import path
from .views import WhiskeyPageView, MandMPageView

app_name = 'whiskeycellar'

urlpatterns = [
    path('jameson/', WhiskeyPageView.as_view(), name='jameson'),
    path('mandm/', MandMPageView.as_view(), name='mandm'),
]
