from django.urls import path
from .views import SignUpView, LoginView, LogoutView


urlpatterns = [
    path('logout', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
