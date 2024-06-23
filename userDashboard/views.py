from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from django.db.models import Sum

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_transactions = Transaction.objects.filter(user=user)
        total_deposited = user_transactions.aggregate(Sum('amount'))['amount__sum']
        total_transactions = Transaction.objects.aggregate(Sum('amount'))['amount__sum']

        return Response({
            "user_total_deposited": total_deposited,
            "total_transactions": total_transactions,
            "user_profit_percentage": (total_deposited / total_transactions) * 100 if total_transactions else 0
        })
