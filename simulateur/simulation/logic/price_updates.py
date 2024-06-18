import logging
from django.utils import timezone
from simulation.models import TransactionHistory

logger = logging.getLogger(__name__)

def update_asset_price(asset):
    asset.price = max(asset.price, 0)
    if asset.open_price == 0:
        asset.open_price = float(asset.price)
    asset.high_price = max(asset.high_price, asset.price)
    asset.low_price = min(asset.low_price, asset.price)
    asset.close_price = float(asset.price)
    asset.save()

def update_ohlc(asset):
    if asset.open_price == 0:
        asset.open_price = float(asset.price)
    asset.high_price = max(asset.high_price, asset.price)
    asset.low_price = min(asset.low_price, asset.price)
    asset.close_price = float(asset.price)
    asset.save()

def log_transactions(transactions):
    for transaction in transactions:
        TransactionHistory.objects.create(
            portfolio=transaction['portfolio'],
            asset=transaction['asset'],
            transaction_type=transaction['transaction_type'],
            amount=transaction['amount'],
            price=transaction['price']
        )
