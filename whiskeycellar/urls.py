from django.urls import path
from .views import JamesonPageView, MandMPageView

app_name = 'whiskeycellar'

urlpatterns = [
    path('jameson/', JamesonPageView.as_view(), name='jameson'),
    path('mandm/', MandMPageView.as_view(), name='mandm'),
]
