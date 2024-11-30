from django.urls import path
from .views import AllWhiskeysPageView, JamesonPageView, MandMPageView, MidletonPageView, PowersPageView, RedBreastPageView, SpotPageView
from . import views

app_name = 'whiskeycellar'

urlpatterns = [
    path('all_whiskeys', AllWhiskeysPageView.as_view(), name='all_whiskeys'),
    path('jameson/', JamesonPageView.as_view(), name='jameson'),
    path('mandm/', MandMPageView.as_view(), name='mandm'),
    path('midleton/', MidletonPageView.as_view(), name='midleton'),
    path('powers/', PowersPageView.as_view(), name='powers'),
    path("red_breast/", RedBreastPageView.as_view(), name='red_breast'),
    path("spot/", SpotPageView.as_view(), name='spot'),
    path("product_detail/<int:product_id>/", views.product_detail, name='product_detail'),
]
