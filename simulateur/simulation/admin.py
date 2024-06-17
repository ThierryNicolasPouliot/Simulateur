from django.contrib import admin
from .models import Company, Stock, Cryptocurrency, UserProfile, Event, Team, SimulationSettings, Scenario, Portfolio, TransactionHistory, Trigger, CustomStat

admin.site.register(Company)
admin.site.register(Stock)
admin.site.register(Cryptocurrency)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(SimulationSettings)
admin.site.register(Scenario)
admin.site.register(Portfolio)
admin.site.register(TransactionHistory)
admin.site.register(Trigger)
admin.site.register(CustomStat)
