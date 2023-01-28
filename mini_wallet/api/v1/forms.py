from django import forms
from django.utils import timezone

from rest_framework.authtoken.models import Token

from mini_wallet.apps.users.models import User

from mini_wallet.apps.wallets.models import Wallet, WalletLog
from mini_wallet.apps.transactions.models import Transaction

from typing import Dict, Any, List


class InitForm(forms.Form):
    xid = forms.CharField()

    def save(self) -> User:
        xid = self.cleaned_data['xid']

        user, created = User.objects.get_or_create(
            xid=xid, defaults={
                "username": xid
            })

        if created:
            wallet = Wallet.objects.create(user=user)
            wallet.logs.create(action=WalletLog.Action.CREATED.value, created_by=user)

            Token.objects.create(user=user)

        return user


class EnableWalletForm(forms.Form):

    def __init__(self, wallet: Wallet, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.wallet = wallet

    def clean(self) -> Dict:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if self.wallet.is_active:
            raise forms.ValidationError("Your wallet is already enabled")

        return cleaned_data

    def save(self) -> Wallet:
        self.wallet.is_active = True
        self.wallet.enabled_at = timezone.now()

        self.wallet.save(update_fields=["is_active", 'enabled_at'])
        self.wallet.logs.create(action=WalletLog.Action.ENABLED.value, created_by=self.wallet.user)

        return self.wallet


class DisableWalletForm(forms.Form):

    def __init__(self, wallet: Wallet, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.wallet = wallet

    def clean(self) -> Dict:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if not self.wallet.is_active:
            raise forms.ValidationError("Your wallet is already disabled")

        return cleaned_data

    def save(self) -> Wallet:
        self.wallet.is_active = False
        self.wallet.disabled_at = timezone.now()

        self.wallet.save(update_fields=["is_active", 'disabled_at'])
        self.wallet.logs.create(action=WalletLog.Action.DISABLED.value, created_by=self.wallet.user)

        return self.wallet


class DepositForm(forms.Form):
    amount = forms.FloatField()
    reference_id = forms.CharField()

    def __init__(self, wallet: Wallet, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.wallet = wallet

    def clean(self) -> Dict:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if not self.wallet.is_active:
            raise forms.ValidationError("Wallet disabled")

        reference_id = cleaned_data['reference_id']
        if Transaction.objects \
            .filter(reference_id=reference_id, status=Transaction.Status.SUCCESS.value,
                    type=Transaction.Type.DEPOSIT.value) \
            .exists():
            raise forms.ValidationError("Deposit with this reference ID is already exist")

        return cleaned_data

    def save(self) -> Transaction:
        amount = self.cleaned_data['amount']
        reference_id = self.cleaned_data['reference_id']

        transaction = self.wallet.transactions.create(
            amount=amount,
            reference_id=reference_id,
            type=Transaction.Type.DEPOSIT.value,
            created_by=self.wallet.user,
            status=Transaction.Status.SUCCESS.value
        )

        self.wallet.balance += amount
        self.wallet.save(update_fields=['balance'])

        return transaction


class WithdrawalForm(forms.Form):
    amount = forms.FloatField()
    reference_id = forms.CharField()

    def __init__(self, wallet: Wallet, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.wallet = wallet

    def clean(self) -> Dict:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if not self.wallet.is_active:
            raise forms.ValidationError("Wallet disabled")

        reference_id = cleaned_data['reference_id']
        amount = cleaned_data['amount']

        if self.wallet.balance < amount:
            raise forms.ValidationError("Insufficient balance")

        if Transaction.objects \
            .filter(reference_id=reference_id, status=Transaction.Status.SUCCESS.value,
                    type=Transaction.Type.WITHDRAWAL.value) \
            .exists():
            raise forms.ValidationError("Withdrawal with this reference ID is already exist")

        return cleaned_data

    def save(self) -> Transaction:
        amount = self.cleaned_data['amount']
        reference_id = self.cleaned_data['reference_id']

        transaction = self.wallet.transactions.create(
            amount=amount,
            reference_id=reference_id,
            type=Transaction.Type.WITHDRAWAL.value,
            created_by=self.wallet.user,
            status=Transaction.Status.SUCCESS.value
        )

        self.wallet.balance -= amount
        self.wallet.save(update_fields=['balance'])

        return transaction
