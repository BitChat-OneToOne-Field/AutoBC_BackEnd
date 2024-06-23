from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from django.db.models import Sum
from .serializers import TransactionSerializer
from rest_framework import status

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_transactions = Transaction.objects.filter(user=user)
        total_deposited = user_transactions.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_withdrawn = user_transactions.filter(transaction_type='withdraw').aggregate(Sum('amount'))['amount__sum'] or 0
        current_balance = total_deposited - total_withdrawn

        total_transactions = Transaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            "user_total_deposited": total_deposited,
            "total_transactions": total_transactions,
            "user_profit_percentage": (total_deposited / total_transactions) * 100 if total_transactions else 0,
            "current_balance": current_balance
        })

class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        if amount and float(amount) > 0:
            transaction = Transaction.objects.create(user=user, amount=amount, transaction_type='deposit')
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
