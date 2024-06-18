from rest_framework import serializers
from .models import Company, SimulationData, Stock, Cryptocurrency, UserProfile, Event, SimulationSettings, Scenario, Team, Portfolio, TransactionHistory, Trigger, CustomStat

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class SimulationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationSettings
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'

class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = '__all__'

class CustomStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomStat
        fields = '__all__'

class ScenarioSerializer(serializers.ModelSerializer):
    companies = CompanySerializer(many=True)
    stocks = StockSerializer(many=True)
    users = UserProfileSerializer(many=True)
    teams = TeamSerializer(many=True)
    events = EventSerializer(many=True)
    triggers = TriggerSerializer(many=True)
    custom_stats = CustomStatSerializer(many=True)

    class Meta:
        model = Scenario
        fields = '__all__'

class SimulationDataSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer()
    user = UserProfileSerializer()
    team = TeamSerializer()
    portfolio = PortfolioSerializer()
    transaction_history = TransactionHistorySerializer(many=True)

    class Meta:
        model = SimulationData
        fields = '__all__'
