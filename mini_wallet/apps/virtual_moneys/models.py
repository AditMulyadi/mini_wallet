from django.db import models


class VirtualMoney(models.Model):
    wallet = models.ForeignKey('wallets.Wallet', related_name="virtual_moneys", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    class Type(models.IntegerChoices):
        DEPOSIT = 1, 'Deposit'
        WITHDRAWAL = 2, 'Withdrawal'

    type = models.PositiveSmallIntegerField(choices=Type.choices)

    class Status(models.IntegerChoices):
        SUCCESS = 1, 'success'
        FAIL = 2, 'fail'

    status = models.PositiveSmallIntegerField(choices=Status.choices)

    created_by = models.ForeignKey('users.User', related_name="virtual_moneys", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    reference_id = models.TextField(null=True)

    def __str__(self) -> str:
        return f"{self.id}"
