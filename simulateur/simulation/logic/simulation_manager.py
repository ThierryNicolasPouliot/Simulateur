import time
import logging
from django.utils import timezone
from channels.layers import get_channel_layer
from simulation.models import Scenario, SimulationData, Stock, Cryptocurrency
from simulation.logic.queue import buy_sell_queue
from simulation.logic.event_handlers import apply_events, apply_triggers, apply_random_fluctuation
from simulation.logic.price_updates import update_asset_price, update_ohlc, log_transactions
from simulation.logic.utils import is_market_open, send_ohlc_update

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

    def __init__(self, scenario_id, run_duration=100000):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.channel_layer = get_channel_layer()
        self.running = False
        self.simulation_data = None
        self.run_duration = run_duration

        settings = self.scenario.simulation_settings
        self.time_step = settings.timer_step * self.TIME_UNITS[settings.timer_step_unit]
        self.interval = settings.interval * self.TIME_UNITS[settings.interval_unit]
        self.close_stock_market_at_night = settings.close_stock_market_at_night
        self.fluctuation_rate = settings.fluctuation_rate
        self.noise_function = settings.noise_function.lower()

        self.stock_prices = {stock.company.name: [] for stock in Stock.objects.all()}
        self.crypto_prices = {crypto.name: [] for crypto in Cryptocurrency.objects.all()}

        logger.info(f'Starting simulation for scenario {self.scenario} with time step {self.time_step} seconds')

    def start_simulation(self):
        self.running = True
        self.simulation_data = SimulationData.objects.create(scenario=self.scenario)
        start_time = timezone.now()
        try:
            while self.running:
                current_time = timezone.now()
                elapsed_time = (current_time - start_time).total_seconds()

                if elapsed_time >= self.run_duration:
                    logger.info('Run duration reached, stopping simulation')
                    break

                if self.close_stock_market_at_night and not is_market_open(current_time):
                    logger.info('Stock market is closed')
                else:
                    self.update_prices(current_time)
                    transactions = buy_sell_queue.process_queues()
                    log_transactions(transactions)
                self.broadcast_updates()
                time.sleep(self.time_step)
        except KeyboardInterrupt:
            logger.info('Simulation stopped by user')
        except Exception as e:
            logger.error(f'Error occurred during simulation: {e}', exc_info=True)
        finally:
            self.stop_simulation()

    def stop_simulation(self):
        if self.simulation_data:
            self.simulation_data.stop_simulation()
        self.running = False
        logger.info('Simulation stopped')

    def update_prices(self, current_time):
        updated_stocks = []
        updated_cryptos = []

        for company in self.scenario.companies.all():
            if stock := company.stock_set.first():
                self.apply_changes(stock, current_time)
                self.stock_prices[stock.company.name].append(stock.close_price)
                updated_stocks.append({
                    'stockName': stock.company.name,
                    'stock': {
                        'price': stock.price,
                        'valueChange': stock.value_change,
                        'valueHistory': stock.value_history,
                        'quantity': stock.quantity
                    }
                })

        for crypto in self.scenario.cryptocurrencies.all():
            self.apply_changes(crypto, current_time)
            self.crypto_prices[crypto.name].append(crypto.close_price)
            updated_cryptos.append({
                'stockName': crypto.name,
                'stock': {
                    'price': crypto.price,
                    'valueChange': crypto.value_change,
                    'valueHistory': crypto.value_history,
                    'quantity': crypto.quantity
                }
            })

        self.simulation_data.end_time = current_time
        self.simulation_data.save()

    def apply_changes(self, asset, current_time):
        apply_events(asset, self.scenario.events.filter(trigger_date__lte=current_time))
        apply_triggers(asset, self.scenario.triggers.all())
        apply_random_fluctuation(asset, self.time_step, self.fluctuation_rate, self.noise_function)
        update_ohlc(asset)

    def broadcast_updates(self):
        for company in self.scenario.companies.all():
            if stock := company.stock_set.first():
                send_ohlc_update(self.channel_layer, stock, 'stock')
        for crypto in self.scenario.cryptocurrencies.all():
            send_ohlc_update(self.channel_layer, crypto, 'cryptocurrency')
