from django.db import models
from django.utils.translation import gettext_lazy as _


class PAIRS(models.TextChoices):
    BRLBTC = "BRLBTC", _("BRL - Bitcoin")
    BRLETH = "BRLETH", _("BRL - Ethereum")


class Historic(models.Model):
    pair = models.CharField(max_length=6, choices=PAIRS.choices)
    timestamp = models.IntegerField()
    price = models.FloatField()
    mms_20 = models.FloatField(blank=True)
    mms_50 = models.FloatField(blank=True)
    mms_200 = models.FloatField(blank=True)

    class Meta:
        ordering = ("timestamp",)

    def __repr__(self):
        return f"Historic({self.pair}, {self.timestamp}, {self.price}, {self.mms_20}, {self.mms_50}, {self.mms_200})"

    def __str__(self):
        return f"{self.pair} - {self.timestamp} - {self.price}"
