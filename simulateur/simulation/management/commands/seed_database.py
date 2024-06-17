# simulation/management/commands/seed_database.py
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from simulation.models import Company, Stock, Cryptocurrency, Team, UserProfile, Event, Trigger, CustomStat, SimulationSettings, Scenario, Portfolio, TransactionHistory

class Command(BaseCommand):
    help = 'Seed the database with initial data from CSV files'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.seed_users()
                self.seed_companies()
                self.seed_stocks()
                self.seed_cryptocurrencies()
                self.seed_teams()
                self.seed_events()
                self.seed_triggers()
                self.seed_custom_stats()
                self.seed_simulation_settings()
                self.seed_scenarios()
                self.seed_portfolios()
                self.seed_transaction_history()
            self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))

    def seed_users(self):
        with open('data/users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user, created = User.objects.get_or_create(
                    username=row['username'],
                    defaults={
                        'email': row['email'],
                        'password': row['password']
                    }
                )
                UserProfile.objects.create(
                    user=user,
                    balance=float(row['balance']),
                    borrowed_money=float(row['borrowed_money'])
                )

    def seed_companies(self):
        with open('data/companies.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Company.objects.create(
                    name=row['name'],
                    backstory=row['backstory'],
                    max_shares=int(row['max_shares']),
                    price_maximum=float(row['price_maximum']),
                    initial_price=float(row['initial_price']),
                    current_price=float(row['current_price'])
                )

    def seed_stocks(self):
        with open('data/stocks.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                company = Company.objects.get(name=row['company'])
                Stock.objects.create(
                    company=company,
                    price=float(row['price']),
                    partial_share=float(row['partial_share']),
                    complete_share=int(row['complete_share']),
                    open_price=float(row['open_price']),
                    high_price=float(row['high_price']),
                    low_price=float(row['low_price']),
                    close_price=float(row['close_price'])
                )

    def seed_cryptocurrencies(self):
        with open('data/cryptocurrencies.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Cryptocurrency.objects.create(
                    name=row['name'],
                    price=float(row['price']),
                    price_maximum=float(row['price_maximum'])
                )

    def seed_teams(self):
        with open('data/teams.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                team = Team.objects.create(
                    name=row['name'],
                    balance=float(row['balance']),
                    borrowed_money=float(row['borrowed_money'])
                )
                members = UserProfile.objects.filter(user__username__in=row['members'].split(';'))
                team.members.set(members)

    def seed_events(self):
        with open('data/events.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Event.objects.create(
                    name=row['name'],
                    description=row['description'],
                    impact=float(row['impact']),
                    event_type=row['event_type'],
                    trigger_date=datetime.strptime(row['trigger_date'], '%Y-%m-%d %H:%M:%S')
                )

    def seed_triggers(self):
        with open('data/triggers.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Trigger.objects.create(
                    name=row['name'],
                    description=row['description'],
                    trigger_type=row['trigger_type'],
                    trigger_value=float(row['trigger_value'])
                )

    def seed_custom_stats(self):
        with open('data/custom_stats.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CustomStat.objects.create(
                    name=row['name'],
                    value=float(row['value'])
                )

    def seed_simulation_settings(self):
        with open('data/simulation_settings.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                SimulationSettings.objects.create(
                    max_users=int(row['max_users']),
                    max_companies=int(row['max_companies']),
                    timer_step=int(row['timer_step']),
                    interval=int(row['interval']),
                    max_interval=int(row['max_interval']),
                    fluctuation_rate=float(row['fluctuation_rate']),
                    time_unit=row['time_unit'],
                    close_stock_market_at_night=row['close_stock_market_at_night']
                )

    def seed_scenarios(self):
        with open('data/scenarios.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                simulation_settings = SimulationSettings.objects.get(id=int(row['simulation_settings']))
                scenario = Scenario.objects.create(
                    name=row['name'],
                    description=row['description'],
                    backstory=row['backstory'],
                    difficulty_level=row['difficulty_level'],
                    duration=int(row['duration']),
                    simulation_settings=simulation_settings
                )
                companies = Company.objects.filter(name__in=row['companies'].split(';'))
                stocks = Stock.objects.filter(company__name__in=row['stocks'].split(';'))
                users = UserProfile.objects.filter(user__username__in=row['users'].split(';'))
                teams = Team.objects.filter(name__in=row['teams'].split(';'))
                events = Event.objects.filter(name__in=row['events'].split(';'))
                triggers = Trigger.objects.filter(name__in=row['triggers'].split(';'))
                custom_stats = CustomStat.objects.filter(name__in=row['custom_stats'].split(';'))
                scenario.companies.set(companies)
                scenario.stocks.set(stocks)
                scenario.users.set(users)
                scenario.teams.set(teams)
                scenario.events.set(events)
                scenario.triggers.set(triggers)
                scenario.custom_stats.set(custom_stats)

    def seed_portfolios(self):
        with open('data/portfolios.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                owner = UserProfile.objects.get(user__username=row['owner']) if row['owner'] else None
                team = Team.objects.get(name=row['team']) if row['team'] else None
                portfolio = Portfolio.objects.create(
                    owner=owner,
                    team=team
                )
                stocks = Stock.objects.filter(company__name__in=row['stocks'].split(';'))
                cryptocurrencies = Cryptocurrency.objects.filter(name__in=row['cryptocurrencies'].split(';'))
                portfolio.stocks.set(stocks)
                portfolio.cryptocurrencies.set(cryptocurrencies)

    def seed_transaction_history(self):
        with open('data/transaction_history.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                portfolio = Portfolio.objects.get(owner__user__username=row['portfolio_owner'])
                TransactionHistory.objects.create(
                    portfolio=portfolio,
                    asset=row['asset'],
                    transaction_type=row['transaction_type'],
                    amount=float(row['amount']),
                    price=float(row['price']),
                    date=datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                )
