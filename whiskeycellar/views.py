from django.views.generic import ListView
from .models import Whiskey

class WhiskeyPageView(ListView):
    model = Whiskey
    template_name = 'jameson.html'
    context_object_name = "jameson_whiskey"
    
class MandMPageView(ListView):
    model = Whiskey
    template_name = 'mandm.html'
    context_object_name = "mandm_whiskey"

