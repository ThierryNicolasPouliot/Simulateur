import random
import time
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from simulation.models import Company, Stock, Cryptocurrency, Event, Scenario, TransactionHistory
from simulation.queue import buy_sell_queue

class SimulationManager:
    def __init__(self, scenario_id):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.channel_layer = get_channel_layer()
        self.running = False

    def start_simulation(self):
        self.running = True
        while self.running:
            self.update_prices()
            buy_sell_queue.process_queues()
            self.broadcast_updates()
            time.sleep(self.scenario.simulation_settings.timer_step)

    def stop_simulation(self):
        self.running = False

    def update_prices(self):
        current_time = timezone.now()
        
        # Update stock prices
        for company in self.scenario.companies.all():
            stock = company.stock_set.first()
            if stock:
                self.apply_events(stock, current_time)
                self.apply_triggers(stock)
                self.apply_random_fluctuation(stock)
                self.update_ohlc(stock)
                stock.save()

        # Update cryptocurrency prices
        for crypto in self.scenario.cryptocurrencies.all():
            self.apply_events(crypto, current_time)
            self.apply_triggers(crypto)
            self.apply_random_fluctuation(crypto)
            self.update_ohlc(crypto)
            crypto.save()

    def apply_events(self, asset, current_time):
        for event in self.scenario.events.filter(trigger_date__lte=current_time):
            asset.price += event.impact
            asset.price = max(0, asset.price)  # Ensure price doesn't go negative

    def apply_triggers(self, asset):
        for trigger in self.scenario.triggers.all():
            if trigger.trigger_type == 'increase' and asset.price > trigger.trigger_value:
                asset.price += trigger.impact
            elif trigger.trigger_type == 'decrease' and asset.price < trigger.trigger_value:
                asset.price -= trigger.impact
            asset.price = max(0, asset.price)  # Ensure price doesn't go negative

    def apply_random_fluctuation(self, asset):
        fluctuation_rate = self.scenario.simulation_settings.fluctuation_rate
        fluctuation = random.uniform(-fluctuation_rate, fluctuation_rate)
        asset.price += fluctuation
        asset.price = max(0, asset.price)  # Ensure price doesn't go negative

    def update_ohlc(self, asset):
        if asset.open_price == 0.0:
            asset.open_price = asset.price
        asset.high_price = max(asset.high_price, asset.price)
        asset.low_price = min(asset.low_price, asset.price)
        asset.close_price = asset.price

    def broadcast_updates(self):
        for company in self.scenario.companies.all():
            stock = company.stock_set.first()
            if stock:
                self.send_ohlc_update(stock)
        for crypto in self.scenario.cryptocurrencies.all():
            self.send_ohlc_update(crypto)

    def send_ohlc_update(self, asset):
        group_name = f'stock_{asset.id}' if isinstance(asset, Stock) else f'crypto_{asset.id}'
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'ohlc_message',
                'data': {
                    'id': asset.id,
                    'open': asset.open_price,
                    'high': asset.high_price,
                    'low': asset.low_price,
                    'close': asset.close_price,
                    'timestamp': timezone.now().isoformat()
                }
            }
        )
