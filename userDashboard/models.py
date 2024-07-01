from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class WithdrawalRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    usdt_address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)