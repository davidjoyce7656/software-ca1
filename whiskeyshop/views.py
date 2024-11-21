from django.views.generic import TemplateView

# View to display all available whiskey

class HomePageView(TemplateView):
    template_name = 'home.html'
    
