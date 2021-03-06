# Generated by Django 3.2.5 on 2021-07-17 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Historic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "pair",
                    models.CharField(choices=[("BRLBTC", "BRL - Bitcoin"), ("BRLETH", "BRL - Ethereum")], max_length=6),
                ),
                ("timestamp", models.IntegerField()),
                ("price", models.FloatField()),
                ("mms_20", models.FloatField(blank=True)),
                ("mms_50", models.FloatField(blank=True)),
                ("mms_200", models.FloatField(blank=True)),
            ],
            options={"ordering": ("timestamp",),},
        ),
    ]
