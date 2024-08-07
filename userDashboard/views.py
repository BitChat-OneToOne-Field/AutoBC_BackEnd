import ccxt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, WithdrawalRequest
from user.models import User
from django.conf import settings
from django.db.models import Sum
from .serializers import TransactionSerializer, WithdrawalRequestSerializer
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

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

class CheckDepositsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        binance = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_SECRET_KEY,
            'enableRateLimit': True,
        })

        try:
            deposits = binance.fetch_deposits('USDT')
            for deposit in deposits:
                user = User.objects.filter(binance_id=deposit['info']['user_id']).first()
                if user:
                    # Check if transaction already exists
                    if not Transaction.objects.filter(transaction_id=deposit['txid']).exists():
                        transaction = Transaction.objects.create(
                            user=user,
                            amount=deposit['amount'],
                            transaction_type='deposit',
                            status='completed',
                            address=deposit['address'],
                            transaction_id=deposit['txid'],
                            created_at=deposit['timestamp']
                        )
                        user.balance += float(deposit['amount'])
                        user.save()
            return Response({"message": "Deposits checked and updated."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error checking deposits: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WithdrawalRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')

        if not amount or float(amount) <= 0:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Assuming user's Binance ID is stored in the user profile
        binance_id = user.binance_id

        withdrawal_request = WithdrawalRequest.objects.create(
            user=user, amount=amount, usdt_address=binance_id, status='pending'
        )

        binance = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_SECRET_KEY,
            'enableRateLimit': True,
        })

        try:
            response = binance.withdraw(
                code='USDT',  
                amount=float(amount),
                address=binance_id,
                tag=None,  
            )

            withdrawal_request.status = 'completed'
            withdrawal_request.save()

            Transaction.objects.create(
                user=user,
                amount=amount,
                transaction_type='withdraw',
                status='completed',
                transaction_id=response['id']  # Save the transaction ID from the withdrawal response
            )

            return Response(WithdrawalRequestSerializer(withdrawal_request).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            withdrawal_request.status = 'failed'
            withdrawal_request.save()
            logger.error(f"Binance API error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

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
