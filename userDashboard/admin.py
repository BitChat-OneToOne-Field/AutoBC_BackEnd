from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__email', 'amount', 'transaction_type')
    ordering = ('-created_at',)

admin.site.register(Transaction, TransactionAdmin)
