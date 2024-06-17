from collections import deque
from datetime import timezone
from django.db import transaction
from simulation.models import TransactionHistory, SimulationData

class BuySellQueue:
    def __init__(self):
        self.buy_queue = deque()
        self.sell_queue = deque()

    def add_to_buy_queue(self, user, asset, amount, price):
        self.buy_queue.append((user, asset, amount, price))

    def add_to_sell_queue(self, user, asset, amount, price):
        self.sell_queue.append((user, asset, amount, price))

    def process_queues(self):
        transactions = []
        while self.buy_queue and self.sell_queue:
            buy_order = self.buy_queue.popleft()
            sell_order = self.sell_queue.popleft()

            # Match the buy and sell orders
            if buy_order[3] >= sell_order[3]:  # Buy price >= Sell price
                matched_price = (buy_order[3] + sell_order[3]) / 2
                transactions.append(self.execute_transaction(buy_order, sell_order, matched_price))
        return transactions

    @transaction.atomic
    def execute_transaction(self, buy_order, sell_order, price):
        buyer, asset, amount, buy_price = buy_order
        seller, _, sell_amount, sell_price = sell_order

        if sell_amount >= amount:
            # Complete the transaction
            seller.portfolio.stocks.remove(asset)
            buyer.portfolio.stocks.add(asset)

            seller.balance += price * amount
            buyer.balance -= price * amount

            seller.save()
            buyer.save()

            # Log the transaction
            transaction = {
                'buyer': buyer.user.username,
                'seller': seller.user.username,
                'asset': asset.name,
                'amount': amount,
                'price': price,
                'timestamp': timezone.now().isoformat()
            }

            TransactionHistory.objects.create(
                portfolio=buyer.portfolio,
                asset=asset.name,
                transaction_type='buy',
                amount=amount,
                price=price
            )

            TransactionHistory.objects.create(
                portfolio=seller.portfolio,
                asset=asset.name,
                transaction_type='sell',
                amount=amount,
                price=price
            )

            # Adjust the remaining sell order if any
            if sell_amount > amount:
                self.add_to_sell_queue(seller, asset, sell_amount - amount, sell_price)
            return transaction
        else:
            # Partial transaction
            seller.portfolio.stocks.remove(asset)
            buyer.portfolio.stocks.add(asset)

            seller.balance += price * sell_amount
            buyer.balance -= price * sell_amount

            seller.save()
            buyer.save()

            # Log the partial transaction
            transaction = {
                'buyer': buyer.user.username,
                'seller': seller.user.username,
                'asset': asset.name,
                'amount': sell_amount,
                'price': price,
                'timestamp': timezone.now().isoformat()
            }

            TransactionHistory.objects.create(
                portfolio=buyer.portfolio,
                asset=asset.name,
                transaction_type='buy',
                amount=sell_amount,
                price=price
            )

            TransactionHistory.objects.create(
                portfolio=seller.portfolio,
                asset=asset.name,
                transaction_type='sell',
                amount=sell_amount,
                price=price
            )

            # Put the remaining buy order back to the queue
            self.add_to_buy_queue(buyer, asset, amount - sell_amount, buy_price)
            return transaction

buy_sell_queue = BuySellQueue()
