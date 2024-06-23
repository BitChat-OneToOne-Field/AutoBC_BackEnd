from django.urls import path
from .views import UserDashboardView, DepositView

urlpatterns = [
    path('userDashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('deposit/', DepositView.as_view(), name='deposit'),
]
