from django.contrib import admin

from .models import Wallet, WalletLog

admin.site.register(Wallet)
admin.site.register(WalletLog)
