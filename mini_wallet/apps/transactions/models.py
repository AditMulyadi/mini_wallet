from django.db import models


class Transaction(models.Model):
    wallet = models.ForeignKey('wallets.Wallet', related_name="transactions", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    class Type(models.IntegerChoices):
        DEPOSIT = 1, 'deposit'
        WITHDRAWAL = 2, 'withdrawal'

    type = models.PositiveSmallIntegerField(choices=Type.choices)

    class Status(models.IntegerChoices):
        SUCCESS = 1, 'success'
        FAIL = 2, 'fail'

    status = models.PositiveSmallIntegerField(choices=Status.choices)

    created_by = models.ForeignKey('users.User', related_name="transactions", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    reference_id = models.TextField(null=True)

    class Meta:
        unique_together = ['type', 'reference_id']

    def __str__(self) -> str:
        return f"{self.id}"
