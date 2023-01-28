from typing import Dict

from mini_wallet.apps.virtual_moneys.models import VirtualMoney


def serialize_wallet(wallet) -> Dict:
    data = {
        "id": wallet.id,
        "owned_by": wallet.user.xid,
        "balance": wallet.balance,
        "status": "enable" if wallet.is_active else "disabled",
    }

    if wallet.enabled_at:
        data["enabled_at"] = wallet.enabled_at.isoformat()

    if wallet.disabled_at:
        data["disabled_at"] = wallet.disabled_at.isoformat()

    return data


def serialize_virtual_money(virtual_money) -> Dict:
    data = {
        "id": virtual_money.id,
        "amount": virtual_money.amount,
        "status": virtual_money.get_status_display(),
        "reference_id": virtual_money.reference_id,
    }

    if virtual_money.type == VirtualMoney.Type.DEPOSIT:
        data["deposited_at"] = virtual_money.created.isoformat()
        data["deposited_by"] = virtual_money.created_by.xid
    else:
        data["withdrawn_at"] = virtual_money.created.isoformat()
        data["withdrawn_by"] = virtual_money.created_by.xid

    return data