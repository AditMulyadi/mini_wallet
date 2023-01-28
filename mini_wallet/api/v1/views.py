from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from mini_wallet.api.response import SuccessResponse, ErrorResponse
from mini_wallet.api.views import TokenAPIView

from mini_wallet.api.serialize import serialize_wallet, serialize_virtual_money

from mini_wallet.apps.virtual_moneys.models import VirtualMoney

from .forms import InitForm, InitWalletForm, DepositForm, WithdrawalForm

from typing import Any


class Init(APIView):

    def post(self, request: Request) -> Response:
        form = InitForm(data=request.POST)

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

        form = InitWalletForm(data=request.POST, wallet=user.wallet)

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

        if not wallet.is_active:
            return ErrorResponse(error="Wallet disabled")

        response = {
            "wallet": serialize_wallet(wallet)
        }

        return SuccessResponse(response)

    def patch(self, request: Request) -> Response:
        user = request.user

        form = InitWalletForm(data=request.POST, wallet=user.wallet)

        if not form.is_valid():
            return ErrorResponse(form=form)

        wallet = form.save()

        response = {
            "walet": serialize_wallet(wallet)
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)

class Deposit(TokenAPIView):

    def post(self, request: Request) -> Response:
        user = request.user

        form = DepositForm(data=request.POST, wallet=user.wallet)

        if not form.is_valid():
            return ErrorResponse(form=form)

        virtual_money = form.save()

        response = {
            "deposit": serialize_virtual_money(virtual_money)
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)


class Withdrawal(TokenAPIView):

    def post(self, request: Request) -> Response:
        user = request.user

        form = WithdrawalForm(data=request.POST, wallet=user.wallet)

        if not form.is_valid():
            return ErrorResponse(form=form)

        virtual_money = form.save()

        response = {
            "withdrawal": serialize_virtual_money(virtual_money)
        }
        return SuccessResponse(response, status=status.HTTP_201_CREATED)


class Transaction(TokenAPIView):

    def get(self, request: Request) -> Response:
        user = request.user
        wallet = user.wallet

        if not wallet.is_active:
            return ErrorResponse(error="Wallet disabled")

        virtual_moneys = user.virtual_moneys \
            .filter(status=VirtualMoney.Status.SUCCESS.value) \
            .order_by('-created')

        response = {
            "transactions": [serialize_virtual_money(virtual_money) for virtual_money in virtual_moneys]
        }

        return SuccessResponse(response, status=status.HTTP_200_OK)
