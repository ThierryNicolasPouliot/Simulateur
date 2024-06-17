import random
import time
from datetime import timedelta, datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from simulation.models import Company, Stock, Cryptocurrency, Event, Scenario, SimulationData, TransactionHistory
from simulation.queue import buy_sell_queue
import logging
import matplotlib.pyplot as plt
from blessed import Terminal

logger = logging.getLogger(__name__)

class SimulationManager:
    TIME_UNITS = {
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'month': 2592000,
        'year': 31536000
    }

    def __init__(self, scenario_id, time_unit='second', run_duration=100000):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.channel_layer = get_channel_layer()
        self.running = False
        self.last_interval_start = timezone.now()
        self.simulation_data = None
        self.time_unit = time_unit
        self.time_step = self.scenario.simulation_settings.timer_step * self.TIME_UNITS[time_unit]
        self.interval = self.scenario.simulation_settings.interval * self.TIME_UNITS[time_unit]
        self.close_stock_market_at_night = self.scenario.simulation_settings.close_stock_market_at_night
        self.run_duration = run_duration  # duration for which the simulation should run
        self.stock_prices = {stock.company.name: [] for stock in Stock.objects.all()}
        self.term = Terminal()

        logger.info(f'Starting simulation for scenario {self.scenario} with time unit {self.time_unit}')

    def start_simulation(self):
        self.running = True
        self.simulation_data = SimulationData.objects.create(scenario=self.scenario)
        plt.ion()
        fig, ax = plt.subplots()
        start_time = timezone.now()
        try:
            while self.running:
                current_time = timezone.now()
                elapsed_time = self.calculate_elapsed_time(current_time)
                logger.info(f'Elapsed time since simulation start: {elapsed_time}')

                if elapsed_time['seconds'] >= self.run_duration:
                    logger.info('Run duration reached, stopping simulation')
                    break

                if self.close_stock_market_at_night and not self.is_market_open(current_time):
                    logger.info('Stock market is closed')
                else:
                    self.update_prices(current_time)
                    transactions = buy_sell_queue.process_queues()
                    self.log_transactions(transactions)
                self.broadcast_updates()
                self.update_graph(ax)
                time.sleep(self.time_step)
        except KeyboardInterrupt:
            logger.info('Simulation stopped by user')
        except Exception as e:
            logger.error(f'Error occurred during simulation: {e}')
        finally:
            self.stop_simulation()
            plt.ioff()
            plt.show()

    def stop_simulation(self):
        if self.simulation_data:
            self.simulation_data.stop_simulation()
        self.running = False
        logger.info('Simulation stopped')

    def calculate_elapsed_time(self, current_time):
        elapsed_time = current_time - self.simulation_data.start_time
        seconds = elapsed_time.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        years = seconds / (60 * 60 * 24 * 365)
        return {
            'seconds': seconds,
            'minutes': minutes,
            'hours': hours,
            'years': years
        }

    def update_prices(self, current_time):
        price_changes = []
        # Check if a new interval has started
        if (current_time - self.last_interval_start).total_seconds() >= self.interval:
            self.reset_ohlc_for_all_assets()
            self.last_interval_start = current_time

        # Update prices for stocks and cryptocurrencies
        for company in self.scenario.companies.all():
            stock = company.stock_set.first()
            if stock:
                self.apply_events(stock, current_time)
                self.apply_triggers(stock)
                self.apply_random_fluctuation(stock, is_stock=True)
                self.update_ohlc(stock)
                price_changes.append(self.log_price_change(stock))
                self.stock_prices[stock.company.name].append(stock.close_price)
                logger.info(f'Updated prices for {stock}')

        for crypto in self.scenario.cryptocurrencies.all():
            self.apply_events(crypto, current_time)
            self.apply_triggers(crypto)
            self.apply_random_fluctuation(crypto, is_stock=False)
            self.update_ohlc(crypto)
            price_changes.append(self.log_price_change(crypto))
            logger.info(f'Updated prices for {crypto}')

        # Update simulation data with current time
        if self.simulation_data:
            self.simulation_data.end_time = current_time
            self.simulation_data.price_changes.extend(price_changes)
            self.simulation_data.save()

    def reset_ohlc_for_all_assets(self):
        for company in self.scenario.companies.all():
            stock = company.stock_set.first()
            if stock:
                self.reset_ohlc(stock)

        for crypto in self.scenario.cryptocurrencies.all():
            self.reset_ohlc(crypto)

    def log_price_change(self, asset):
        price_change = {
            'id': asset.id,
            'name': asset.company.name if isinstance(asset, Stock) else asset.name,
            'type': 'Stock' if isinstance(asset, Stock) else 'Cryptocurrency',
            'open': asset.open_price,
            'high': asset.high_price,
            'low': asset.low_price,
            'close': asset.close_price,
            'timestamp': timezone.now().isoformat()
        }
        logger.info(f'Price change logged: {price_change}')
        return price_change

    def reset_ohlc(self, asset):
        asset.open_price = asset.close_price
        asset.high_price = asset.close_price
        asset.low_price = asset.close_price

    def apply_events(self, asset, current_time):
        for event in self.scenario.events.filter(trigger_date__lte=current_time):
            asset.price += event.impact
            asset.price = max(0, asset.price)  # Ensure price doesn't go negative
            logger.info(f'Applied event {event} to {asset}')

    def apply_triggers(self, asset):
        for trigger in self.scenario.triggers.all():
            if trigger.trigger_type == 'increase' and asset.price > trigger.trigger_value:
                asset.price += trigger.impact
            elif trigger.trigger_type == 'decrease' and asset.price < trigger.trigger_value:
                asset.price -= trigger.impact
            asset.price = max(0, asset.price)  # Ensure price doesn't go negative
            logger.info(f'Applied trigger {trigger} to {asset}')

    def apply_random_fluctuation(self, asset, is_stock=True):
        fluctuation_rate = self.scenario.simulation_settings.fluctuation_rate
        fluctuation = random.uniform(-fluctuation_rate * 100, fluctuation_rate * 100)

        # Apply random spike for stocks
        if is_stock and random.random() < 0.01:  # 1% chance of a random spike
            spike = random.uniform(1.5, 2.0)
            fluctuation *= spike
            logger.info(f'Applied random spike to {asset}')

        asset.price += fluctuation

        # Update OHLC prices
        if asset.open_price == 0.0:
            asset.open_price = asset.price
        asset.high_price = max(asset.high_price, asset.price)
        asset.low_price = min(asset.low_price, asset.price)
        asset.close_price = asset.price
        logger.info(f'Applied random fluctuation to {asset}')

    def update_ohlc(self, asset):
        current_price = asset.price
        asset.high_price = max(asset.high_price, current_price)
        asset.low_price = min(asset.low_price, current_price)
        asset.close_price = current_price

    def log_transactions(self, transactions):
        for transaction in transactions:
            TransactionHistory.objects.create(
                portfolio=transaction['portfolio'],
                asset=transaction['asset'],
                transaction_type=transaction['transaction_type'],
                amount=transaction['amount'],
                price=transaction['price']
            )
            logger.info(f'Logged transaction: {transaction}')

    def is_market_open(self, current_time):
        # Assume market is open from 9 AM to 4 PM
        open_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
        close_time = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
        return open_time <= current_time <= close_time

    def broadcast_updates(self):
        for company in self.scenario.companies.all():
            stock = company.stock_set.first()
            if stock:
                self.send_ohlc_update(stock)
        for crypto in self.scenario.cryptocurrencies.all():
            self.send_ohlc_update(crypto)

    def send_ohlc_update(self, asset):
        group_name = 'simulation_updates'
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'simulation_update',
                'data': {
                    'id': asset.id,
                    'name': asset.company.name if isinstance(asset, Stock) else asset.name,
                    'type': 'Stock' if isinstance(asset, Stock) else 'Cryptocurrency',
                    'open': asset.open_price,
                    'high': asset.high_price,
                    'low': asset.low_price,
                    'close': asset.close_price,
                    'timestamp': timezone.now().isoformat()
                }
            }
        )
        logger.info(f'Sent OHLC update for {asset}')

    def update_graph(self, ax):
        ax.clear()
        for company, prices in self.stock_prices.items():
            ax.plot(prices, label=company)
        ax.legend()
        plt.pause(0.05)
        for _ in range(10):
            print(self.term.move_up, end='')

