from django.urls import path
from .views import UserDashboardView, DepositView, WithdrawalRequestView, TransactionHistoryView, PendingWithdrawalsView

urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawalRequestView.as_view(), name='withdraw'),
    path('transactions/', TransactionHistoryView.as_view(), name='transactions'),
    path('withdrawals/pending/', PendingWithdrawalsView.as_view(), name='pending-withdrawals'),
    path('withdrawals/pending/<int:pk>/', PendingWithdrawalsView.as_view(), name='update-withdrawal'),
]
