from django.contrib import admin
from .models import (
    Company, Stock, Cryptocurrency, UserProfile, Event, Team,
    SimulationSettings, Scenario, Portfolio, TransactionHistory,
    Trigger, CustomStat, SimulationData
)
from django import forms
from django_json_widget.widgets import JSONEditorWidget

class SimulationDataAdminForm(forms.ModelForm):
    class Meta:
        model = SimulationData
        fields = '__all__'
        widgets = {
            'price_changes': JSONEditorWidget(attrs={'style': 'width: auto; height: 500px;'}),
            'transactions': JSONEditorWidget(attrs={'style': 'width: auto; height: 500px;'}),
        }

class SimulationDataAdmin(admin.ModelAdmin):
    form = SimulationDataAdminForm

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
admin.site.register(SimulationData, SimulationDataAdmin)
