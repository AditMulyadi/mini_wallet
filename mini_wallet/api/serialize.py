from typing import Dict

from mini_wallet.apps.transactions.models import Transaction


def serialize_wallet(wallet) -> Dict:
    data = {
        "id": wallet.id,
        "owned_by": wallet.user.xid,
        "balance": wallet.balance,
        "status": "enable" if wallet.is_active else "disabled",
    }

    if wallet.enabled_at and wallet.is_active:
        data["enabled_at"] = wallet.enabled_at.isoformat()

    if wallet.disabled_at and not wallet.is_active:
        data["disabled_at"] = wallet.disabled_at.isoformat()

    return data


def serialize_transaction(transaction) -> Dict:
    data = {
        "id": transaction.id,
        "amount": transaction.amount,
        "status": transaction.get_status_display(),
        "reference_id": transaction.reference_id,
        "type": transaction.get_type_display()
    }

    if transaction.type == Transaction.Type.DEPOSIT:
        data["deposited_at"] = transaction.created.isoformat()
        data["deposited_by"] = transaction.created_by.xid
    else:
        data["withdrawn_at"] = transaction.created.isoformat()
        data["withdrawn_by"] = transaction.created_by.xid

    return data