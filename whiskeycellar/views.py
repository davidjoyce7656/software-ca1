from django.views.generic import ListView
from .models import Whiskey

class AllWhiskeysPageView(ListView):
    model = Whiskey
    template_name = 'all_whiskeys.html'
    context_object_name = 'all_whiskeys'

class JamesonPageView(ListView):
    model = Whiskey
    template_name = 'jameson.html'
    context_object_name = "jameson_whiskey"
    
class MandMPageView(ListView):
    model = Whiskey
    template_name = 'mandm.html'
    context_object_name = "mandm_whiskey"

class MidletonPageView(ListView):
    model = Whiskey
    template_name = 'midleton.html'
    context_object_name = "midleton_whiskey"
    
class PowersPageView(ListView):
    model = Whiskey
    template_name = 'powers.html'
    context_object_name = "powers_whiskey"
    
class RedBreastPageView(ListView):
    model = Whiskey
    template_name = 'red_breast.html'
    context_object_name = "red_breast_whiskey"

class SpotPageView(ListView):
    model = Whiskey
    template_name = 'spot.html'
    context_object_name = "spot_whiskey"