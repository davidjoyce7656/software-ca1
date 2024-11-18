from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser

class LoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        return reverse_lazy('whiskeyshop:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('whiskeyshop:home')

    def form_valid(self, form):
        # Save the new user
        response = super().form_valid(form)
        # Add user to the Customer group
        customer_group, created = Group.objects.get_or_create(name='Customer')
        self.object.groups.add(customer_group)
        # Log the user in after signup
        
        login(self.request, self.object)
        
        return response # Redirect to success URL

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        
        return redirect('whiskeyshop:home')