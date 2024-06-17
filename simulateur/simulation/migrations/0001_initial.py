# Generated by Django 5.0.6 on 2024-06-17 16:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("backstory", models.TextField(default="")),
                ("max_shares", models.IntegerField(default=1000)),
                ("price_maximum", models.FloatField(default=0.0)),
                ("initial_price", models.FloatField(default=0.0)),
                ("current_price", models.FloatField(default=0.0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Cryptocurrency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("price", models.FloatField(default=0.0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("price_maximum", models.FloatField(default=0.0)),
                ("open_price", models.FloatField(default=0.0)),
                ("high_price", models.FloatField(default=0.0)),
                ("low_price", models.FloatField(default=0.0)),
                ("close_price", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="CustomStat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("value", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("description", models.TextField(default="")),
                ("impact", models.FloatField(default=0.0)),
                ("event_type", models.CharField(default="", max_length=100)),
                ("trigger_date", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="SimulationSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("max_users", models.IntegerField(default=100)),
                ("max_companies", models.IntegerField(default=50)),
                ("timer_step", models.IntegerField(default=1)),
                ("fluctuation_rate", models.FloatField(default=0.1)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("balance", models.FloatField(default=100000)),
                ("borrowed_money", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Trigger",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("description", models.TextField(default="")),
                ("trigger_type", models.CharField(default="", max_length=100)),
                ("trigger_value", models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.FloatField(default=0.0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("partial_share", models.FloatField(default=0.0)),
                ("complete_share", models.IntegerField(default=0)),
                ("open_price", models.FloatField(default=0.0)),
                ("high_price", models.FloatField(default=0.0)),
                ("low_price", models.FloatField(default=0.0)),
                ("close_price", models.FloatField(default=0.0)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="simulation.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Portfolio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cryptocurrencies",
                    models.ManyToManyField(to="simulation.cryptocurrency"),
                ),
                ("stocks", models.ManyToManyField(to="simulation.stock")),
                (
                    "team",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="portfolio",
                        to="simulation.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TransactionHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("asset", models.CharField(default="", max_length=100)),
                ("transaction_type", models.CharField(default="", max_length=100)),
                ("amount", models.FloatField(default=0.0)),
                ("price", models.FloatField(default=0.0)),
                ("date", models.DateTimeField(auto_now=True)),
                (
                    "portfolio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="simulation.portfolio",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("balance", models.FloatField(default=10000)),
                ("borrowed_money", models.FloatField(default=0.0)),
                (
                    "team",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profiles",
                        to="simulation.team",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(
                related_name="teams", to="simulation.userprofile"
            ),
        ),
        migrations.CreateModel(
            name="Scenario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("description", models.TextField(default="")),
                ("backstory", models.TextField(default="")),
                ("difficulty_level", models.CharField(default="", max_length=100)),
                ("duration", models.IntegerField(default=0)),
                ("companies", models.ManyToManyField(to="simulation.company")),
                ("custom_stats", models.ManyToManyField(to="simulation.customstat")),
                ("events", models.ManyToManyField(to="simulation.event")),
                (
                    "simulation_settings",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="simulation.simulationsettings",
                    ),
                ),
                ("stocks", models.ManyToManyField(to="simulation.stock")),
                ("teams", models.ManyToManyField(to="simulation.team")),
                ("triggers", models.ManyToManyField(to="simulation.trigger")),
                ("users", models.ManyToManyField(to="simulation.userprofile")),
            ],
        ),
        migrations.AddField(
            model_name="portfolio",
            name="owner",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="portfolio",
                to="simulation.userprofile",
            ),
        ),
    ]
