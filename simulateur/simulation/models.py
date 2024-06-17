# simulation/models.py
from datetime import timedelta, timezone, datetime
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    backstory = models.TextField(default='')
    max_shares = models.IntegerField(default=1000)
    price_maximum = models.FloatField(default=0.0)
    initial_price = models.FloatField(default=0.0)
    current_price = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    pe_ratio = models.FloatField(default=0.0)
    market_cap = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
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

    class Meta:
        verbose_name_plural = "Stocks"

class Cryptocurrency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    price = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    price_maximum = models.FloatField(default=0.0)
    partial_share = models.FloatField(default=0.0)
    complete_share = models.IntegerField(default=0)
    open_price = models.FloatField(default=0.0)
    high_price = models.FloatField(default=0.0)
    low_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cryptocurrencies"

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    balance = models.FloatField(default=100000)
    borrowed_money = models.FloatField(default=0.0)
    members = models.ManyToManyField('UserProfile', related_name='teams')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Teams"

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='user_profiles')
    borrowed_money = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Profiles"

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    impact = models.FloatField(default=0.0)
    event_type = models.CharField(max_length=100, default='')
    trigger_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events"

class Trigger(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    trigger_type = models.CharField(max_length=100, default='')
    trigger_value = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Triggers"

class CustomStat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    value = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Custom Stats"

class SimulationSettings(models.Model):
    TIME_UNIT_CHOICES = [
        ('second', 'Second'),
        ('minute', 'Minute'),
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('month', 'Month'),
        ('year', 'Year')
    ]

    id = models.AutoField(primary_key=True)
    max_users = models.IntegerField(default=100)
    max_companies = models.IntegerField(default=50)
    timer_step = models.IntegerField(default=10)
    timer_step_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    interval = models.IntegerField(default=20)
    interval_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    max_interval = models.IntegerField(default=3000)  # Maximum interval in seconds
    fluctuation_rate = models.FloatField(default=0.1)  # Rate of random fluctuation
    time_unit = models.CharField(max_length=6, choices=TIME_UNIT_CHOICES, default='minute')
    close_stock_market_at_night = models.BooleanField(default=True)  # New field

    def __str__(self):
        return f'Simulation Settings:\n' \
               f'  Max users: {self.max_users}\n' \
               f'  Max companies: {self.max_companies}\n' \
               f'  Timer step: {self.timer_step} {self.get_timer_step_unit_display()}\n' \
               f'  Interval: {self.interval} {self.get_interval_unit_display()}\n' \
               f'  Max interval: {self.max_interval} seconds\n' \
               f'  Fluctuation rate: {self.fluctuation_rate}\n' \
               f'  Time unit: {self.get_time_unit_display()}\n' \
               f'  Close stock market at night: {"Yes" if self.close_stock_market_at_night else "No"}'

    class Meta:
        verbose_name_plural = "Simulation Settings"



class Scenario(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    backstory = models.TextField(default='')
    difficulty_level = models.CharField(max_length=100, default='')
    duration = models.IntegerField(default=0)  # Duration in seconds
    companies = models.ManyToManyField(Company)
    stocks = models.ManyToManyField(Stock)
    cryptocurrencies = models.ManyToManyField(Cryptocurrency)
    users = models.ManyToManyField(UserProfile)
    teams = models.ManyToManyField(Team)
    events = models.ManyToManyField(Event)
    triggers = models.ManyToManyField(Trigger)
    custom_stats = models.ManyToManyField(CustomStat)
    simulation_settings = models.OneToOneField(SimulationSettings, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_companies(self):
        return ', '.join([company.name for company in self.companies.all()])

    def get_stocks(self):
        return ', '.join([stock.company.name for stock in self.stocks.all()])

    def get_users(self):
        return ', '.join([user.user.username for user in self.users.all()])

    def get_teams(self):
        return ', '.join([team.name for team in self.teams.all()])

    class Meta:
        verbose_name_plural = "Scenarios"


class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='portfolio')
    stocks = models.ManyToManyField(Stock)
    cryptocurrencies = models.ManyToManyField(Cryptocurrency)

    def __str__(self):
        return f'Portfolio for {self.owner or self.team}'

    def get_stocks(self):
        return ', '.join([stock.company.name for stock in self.stocks.all()])

    def get_cryptocurrencies(self):
        return ', '.join([crypto.name for crypto in self.cryptocurrencies.all()])

    class Meta:
        verbose_name_plural = "Portfolios"

class TransactionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.CharField(max_length=100, default='')
    transaction_type = models.CharField(max_length=100, default='')
    amount = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction on {self.asset}'

    class Meta:
        verbose_name_plural = "Transaction Histories"

class SimulationData(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_changes = models.JSONField(default=list)  # Storing price changes as a JSON field
    transactions = models.JSONField(default=list)  # Storing transactions as a JSON field

    def __str__(self):
        return f'Simulation for {self.scenario.name}'

    def stop_simulation(self):
        self.end_time = datetime.now(timezone.utc)
        self.is_active = False
        self.save()

    @property
    def duration(self):
        if self.is_active:
            return timezone.now() - self.start_time
        elif self.end_time:
            return self.end_time - self.start_time
        else:
            return timedelta(seconds=0)

    def display_price_changes(self):
        return self.price_changes

    display_price_changes.short_description = 'Price Changes'

    class Meta:
        verbose_name_plural = "Simulation Data"
