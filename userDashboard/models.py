from django.db import models
from user.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')], default='deposit')

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.timestamp} - {self.transaction_type}"
