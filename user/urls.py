from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns = [
    path('userRegistration/', UserRegistrationView.as_view(), name='user-registration'),
    path('userLogin/', UserLoginView.as_view(), name='user-login'),
    path('userLogout/', UserLogoutView.as_view(), name='user-logout'),
]
