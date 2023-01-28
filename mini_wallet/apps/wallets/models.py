from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField('users.User', related_name="wallet", on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    is_active = models.BooleanField(default=False)
    enabled_at = models.DateTimeField(blank=True, null=True)
    disabled_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id}"


class WalletLog(models.Model):
    wallet = models.ForeignKey(Wallet, related_name="logs", on_delete=models.CASCADE)

    class Action(models.IntegerChoices):
        CREATED = 1, 'Created'
        ENABLED = 2, 'Enabled'
        DISABLED = 3, 'Disabled'

    action = models.PositiveSmallIntegerField(choices=Action.choices)

    created_by = models.ForeignKey('users.User', related_name="wallet_logs", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(default="", blank=True)

    def __str__(self) -> str:
        return f"{self.id}"
