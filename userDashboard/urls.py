from django.urls import path
from .views import UserDashboardView, GenerateDepositAddressView, CheckDepositsView, WithdrawalRequestView, TransactionHistoryView, PendingWithdrawalsView

urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('generate-deposit-address/', GenerateDepositAddressView.as_view(), name='generate-deposit-address'),
    path('check-deposits/', CheckDepositsView.as_view(), name='check-deposits'),
    path('withdraw/', WithdrawalRequestView.as_view(), name='withdraw'),
    path('transactions/', TransactionHistoryView.as_view(), name='transactions'),
    path('withdrawals/pending/', PendingWithdrawalsView.as_view(), name='pending-withdrawals'),
    path('withdrawals/pending/<int:pk>/', PendingWithdrawalsView.as_view(), name='update-withdrawal'),
]
