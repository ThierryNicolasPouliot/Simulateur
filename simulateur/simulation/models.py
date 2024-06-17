from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100, default='')
    backstory = models.TextField(default='')
    max_shares = models.IntegerField(default=1000)
    price_maximum = models.FloatField(default=0.0)
    initial_price = models.FloatField(default=0.0)
    current_price = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    partial_share = models.FloatField(default=0.0)
    complete_share = models.IntegerField(default=0)
    open_price = models.FloatField(default=0.0)
    high_price = models.FloatField(default=0.0)
    low_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.company.name} Stock'

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100, default='')
    price = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    price_maximum = models.FloatField(default=0.0)
    open_price = models.FloatField(default=0.0)
    high_price = models.FloatField(default=0.0)
    low_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    balance = models.FloatField(default=100000)
    borrowed_money = models.FloatField(default=0.0)
    members = models.ManyToManyField('UserProfile', related_name='teams')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='user_profiles')
    borrowed_money = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    impact = models.FloatField(default=0.0)
    event_type = models.CharField(max_length=100, default='')
    trigger_date = models.DateTimeField()

    def __str__(self):
        return self.name

class Trigger(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    trigger_type = models.CharField(max_length=100, default='')
    trigger_value = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class CustomStat(models.Model):
    name = models.CharField(max_length=100, default='')
    value = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class SimulationSettings(models.Model):
    max_users = models.IntegerField(default=100)
    max_companies = models.IntegerField(default=50)
    timer_step = models.IntegerField(default=1)  # Timer step in seconds
    fluctuation_rate = models.FloatField(default=0.1)  # Rate of random fluctuation

    def __str__(self):
        return f'Simulation Settings (Max Users: {self.max_users}, Max Companies: {self.max_companies})'

class Scenario(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    backstory = models.TextField(default='')
    difficulty_level = models.CharField(max_length=100, default='')
    duration = models.IntegerField(default=0)  # Duration in seconds
    companies = models.ManyToManyField(Company)
    stocks = models.ManyToManyField(Stock)
    users = models.ManyToManyField(UserProfile)
    teams = models.ManyToManyField(Team)
    events = models.ManyToManyField(Event)
    triggers = models.ManyToManyField(Trigger)
    custom_stats = models.ManyToManyField(CustomStat)
    simulation_settings = models.OneToOneField(SimulationSettings, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    stocks = models.ManyToManyField(Stock)
    cryptocurrencies = models.ManyToManyField(Cryptocurrency)

class TransactionHistory(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.CharField(max_length=100, default='')
    transaction_type = models.CharField(max_length=100, default='')
    amount = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction on {self.asset}'
