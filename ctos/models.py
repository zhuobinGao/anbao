from django.db import models

class er_truck(models.Model):
    truckid = models.IntegerField(primary_key=True)
    truckheadweight = models.FloatField()

