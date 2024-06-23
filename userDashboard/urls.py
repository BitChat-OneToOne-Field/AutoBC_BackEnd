from django.urls import path
from .views import UserDashboardView

urlpatterns = [
    path('userDashboard/', UserDashboardView.as_view(), name='user-dashboard'),
]
