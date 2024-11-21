from django.views.generic import ListView
from .models import Whiskey

class WhiskeyPageView(ListView):
    model = Whiskey
    template_name = 'jameson.html'
    context_object_name = "all_whiskeys"
    

