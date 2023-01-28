from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from mini_wallet.api.response import SuccessResponse, ErrorResponse
from mini_wallet.api.views import TokenAPIView

from mini_wallet.api.serialize import serialize_wallet, serialize_transaction

from mini_wallet.apps.transactions.models import Transaction

from .forms import InitForm, DepositForm, WithdrawalForm, EnableWalletForm, DisableWalletForm

from typing import Any


class Init(APIView):

    def post(self, request: Request) -> Response:
        form = InitForm(data=request.data)

        if not form.is_valid():
            return ErrorResponse(form=form)

        user = form.save()

        response = {
            "token": user.auth_token.key
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)


class Wallet(TokenAPIView):

    def post(self, request: Request) -> Response:
        user = request.user

        form = EnableWalletForm(data=request.data, wallet=user.wallet)

        if not form.is_valid():
            return ErrorResponse(form=form)

        wallet = form.save()

        response = {
            "walet": serialize_wallet(wallet)
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        user = request.user
        wallet = user.wallet

        response = {
            "wallet": serialize_wallet(wallet)
        }

        return SuccessResponse(response)

    def patch(self, request: Request) -> Response:
        user = request.user

        form = DisableWalletForm(data=request.data, wallet=user.wallet)

        if not form.is_valid():
            return ErrorResponse(form=form)

        wallet = form.save()

        response = {
            "wallet": serialize_wallet(wallet)
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)


class Deposit(TokenAPIView):

    def post(self, request: Request) -> Response:
        user = request.user

        form = DepositForm(data=request.data, wallet=user.wallet)

        if not form.is_valid():
            return ErrorResponse(form=form)

        transaction = form.save()

        response = {
            "deposit": serialize_transaction(transaction)
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)


class Withdrawal(TokenAPIView):

    def post(self, request: Request) -> Response:
        user = request.user

        form = WithdrawalForm(data=request.data, wallet=user.wallet)

        if not form.is_valid():
            return ErrorResponse(form=form)

        transaction = form.save()

        response = {
            "withdrawal": serialize_transaction(transaction)
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)


class TransactionList(TokenAPIView):

    def get(self, request: Request) -> Response:
        user = request.user
        wallet = user.wallet

        if not wallet.is_active:
            return ErrorResponse(error="Wallet disabled")

        transactions = user.transactions \
            .filter(status=Transaction.Status.SUCCESS.value) \
            .order_by('-created')

        response = {
            "transactions": [serialize_transaction(transaction) for transaction in transactions]
        }

        return SuccessResponse(response, status=status.HTTP_200_OK)
