from django.db import models

# Create your models here.


class Visitors(models.Model):
    timestamp = models.DateTimeField()
    flr_email = models.CharField(max_length=64)
    count = models.IntegerField()
    location = models.CharField(max_length=64)

    capacity = models.FloatField(null=True)
