from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'age',)  # add custom fields like age

class CustomUserChangeForm(UserChangeForm):
    age = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age',)
