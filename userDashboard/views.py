from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, WithdrawalRequest
from user.models import User
from django.db.models import Sum
from .serializers import TransactionSerializer, WithdrawalRequestSerializer
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
        profit_percentage = ((total_deposited / total_transactions) * 100) if total_transactions > 0 else 0

        return Response({
            "total_deposited": total_deposited,
            "total_withdrawn": total_withdrawn,
            "current_balance": current_balance,
            "profit_percentage": profit_percentage
        })

class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        if amount and float(amount) > 0:
            transaction = Transaction.objects.create(user=user, amount=amount, transaction_type='deposit')
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        # Logic to process the deposit via the bot can be added here (Maybe)
        return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
    
class WithdrawalRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        usdt_address = request.data.get('usdt_address')
        
        if not usdt_address:
            usdt_address = user.usdt_address

        withdrawal_request = WithdrawalRequest.objects.create(
            user=user,
            amount=amount,
            usdt_address=usdt_address
        )
        
        # Here you can add logic to send this request to the trading bot for processing
        
        return Response({"status": "Withdrawal request submitted"}, status=status.HTTP_201_CREATED)

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


'''
=================== For Bot Comunication ======================================
'''

class PendingWithdrawalsView(APIView):
    def get(self, request):
        pending_withdrawals = WithdrawalRequest.objects.filter(status='pending')
        serializer = WithdrawalRequestSerializer(pending_withdrawals, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        withdrawal_request = WithdrawalRequest.objects.get(pk=pk)
        serializer = WithdrawalRequestSerializer(withdrawal_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
