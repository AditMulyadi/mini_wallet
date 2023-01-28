from django.urls import path, include

from .views import Init, Wallet, Deposit, Withdrawal, Transaction


app_name = "v1"

urlpatterns = [
    path('init', Init.as_view(), name="init"),
    path('wallet', Wallet.as_view(), name="wallet"),
    path('wallet/deposits', Deposit.as_view(), name="wallet"),
    path('wallet/withdrawals', Withdrawal.as_view(), name="withdrawals"),
    path('wallet/transactions', Transaction.as_view(), name="transactions")
]
