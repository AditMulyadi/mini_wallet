from django import forms
from django.utils import timezone

from rest_framework.authtoken.models import Token

from mini_wallet.apps.users.models import User

from mini_wallet.apps.wallets.models import Wallet, WalletLog
from mini_wallet.apps.virtual_moneys.models import VirtualMoney

from typing import Dict, Any, List


class InitForm(forms.Form):
    xid = forms.CharField()

    def save(self) -> User:
        xid = self.cleaned_data['xid']

        user, created = User.objects.get_or_create(xid=xid)

        if created:
            wallet = Wallet.objects.create(user=user)
            wallet.logs.create(action=WalletLog.Action.CREATED.value, created_by=user)

            Token.objects.create(user=user)

        return user


class InitWalletForm(forms.Form):
    is_disabled = forms.BooleanField(required=False)

    def __init__(self, wallet: Wallet, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.wallet = wallet

    def clean(self) -> Dict:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        is_disabled = cleaned_data['is_disabled']

        if is_disabled and not self.wallet.is_active:
            raise forms.ValidationError("Your wallet is already disabled")
        elif not is_disabled and self.wallet.is_active:
            raise forms.ValidationError("Your wallet is already enabled")

        return cleaned_data

    def save(self) -> Wallet:
        is_disabled = self.cleaned_data['is_disabled']

        if is_disabled:  # Disabled wallet
            self.wallet.is_active = False
            self.wallet.disabled_at = timezone.now()
            action = WalletLog.Action.DISABLED.value

            update_fields = ["is_active", "disabled_at"]

        else:  # Enable Wallet
            self.wallet.is_active = True
            self.wallet.enabled_at = timezone.now()
            action = WalletLog.Action.ENABLED.value

            update_fields = ["is_active", "enabled_at"]

        self.wallet.save(update_fields=update_fields)
        self.wallet.logs.create(action=action, created_by=self.wallet.user)

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
        if VirtualMoney.objects.filter(reference_id=reference_id, status=VirtualMoney.Status.SUCCESS.value).exists():
            raise forms.ValidationError("Transaction with this reference ID is already exist")

        return cleaned_data

    def save(self) -> VirtualMoney:
        amount = self.cleaned_data['amount']
        reference_id = self.cleaned_data['reference_id']

        virtual_money = self.wallet.virtual_moneys.create(
            amount=amount,
            reference_id=reference_id,
            type=VirtualMoney.Type.DEPOSIT.value,
            created_by=self.wallet.user,
            status=VirtualMoney.Status.SUCCESS.value
        )

        self.wallet.balance += amount
        self.wallet.save(update_fields=['balance'])

        return virtual_money


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

        if VirtualMoney.objects.filter(reference_id=reference_id, status=VirtualMoney.Status.SUCCESS.value).exists():
            raise forms.ValidationError("Transaction with this reference ID is already exist")

        return cleaned_data

    def save(self) -> VirtualMoney:
        amount = self.cleaned_data['amount']
        reference_id = self.cleaned_data['reference_id']

        virtual_money = self.wallet.virtual_moneys.create(
            amount=amount,
            reference_id=reference_id,
            type=VirtualMoney.Type.WITHDRAWAL.value,
            created_by=self.wallet.user,
            status=VirtualMoney.Status.SUCCESS.value
        )

        self.wallet.balance -= amount
        self.wallet.save(update_fields=['balance'])

        return virtual_money
