# simulation/logic/price_update.py

import random
import numpy as np
import noise
import logging
from django.utils import timezone
from simulation.models import TransactionHistory

logger = logging.getLogger(__name__)

def apply_events(asset, events):
    for event in events:
        asset.price += event.impact
        asset.price = max(0, asset.price)
        logger.info(f'Applied event {event} to {asset}')

def apply_triggers(asset, triggers):
    for trigger in triggers:
        if trigger.trigger_type == 'increase' and asset.price > trigger.trigger_value:
            asset.price += trigger.impact
        elif trigger.trigger_type == 'decrease' and asset.price < trigger.trigger_value:
            asset.price -= trigger.impact
        asset.price = max(0, asset.price)
        logger.info(f'Applied trigger {trigger} to {asset}')

def apply_random_fluctuation(asset, time_step, fluctuation_rate, noise_function):
    dt = time_step / (24 * 3600)  # Convert time step to days
    noise_functions = {
        'brownian': apply_brownian_motion,
        'monte_carlo': apply_monte_carlo,
        'perlin': apply_perlin_noise,
        'other': apply_other_noise
    }
    noise_func = noise_functions.get(noise_function, apply_other_noise)
    noise_func(asset, dt, fluctuation_rate)

def apply_brownian_motion(asset, dt, fluctuation_rate):
    mu, sigma = 0.001, 0.02
    if random.random() < 0.01:
        sigma *= 10
    random_shock = np.random.normal(0, sigma * np.sqrt(dt))
    price_change = (mu - 0.5 * sigma**2) * dt + random_shock
    asset.price *= np.exp(price_change)

def apply_monte_carlo(asset, dt, fluctuation_rate):
    mu, sigma = 0.001, 0.02
    random_shock = np.random.normal(mu * dt, sigma * np.sqrt(dt))
    asset.price += random_shock

def apply_perlin_noise(asset, dt, fluctuation_rate):
    time = dt * len(asset.value_history)
    perlin_value = noise.pnoise1(time * fluctuation_rate)
    asset.price += perlin_value

def apply_other_noise(asset, dt, fluctuation_rate):
    random_fluctuation = np.random.normal(0, fluctuation_rate * np.sqrt(dt))
    asset.price += random_fluctuation

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