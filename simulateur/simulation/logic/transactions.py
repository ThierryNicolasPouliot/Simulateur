import logging
from simulation.models import TransactionHistory

logger = logging.getLogger(__name__)

def log_transactions(transactions):
    for transaction in transactions:
        TransactionHistory.objects.create(
            portfolio=transaction['portfolio'],
            asset=transaction['asset'],
            transaction_type=transaction['transaction_type'],
            amount=transaction['amount'],
            price=transaction['price']
        )
