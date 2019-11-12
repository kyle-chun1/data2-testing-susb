from django.db import models


class RawMaterialMovement(models.Model):
    rName = models.CharField(max_length=128)
    rDate = models.DateField()
    rMode = models.CharField(max_length=128)
    rTrips = models.CharField(max_length=128)
    rOrigin = models.CharField(max_length=128)
    rOriginLocation = models.CharField(max_length=128)
    rDestination = models.CharField(max_length=128)
    rDestinationLocation = models.CharField(max_length=128)
    rMaterial = models.CharField(max_length=2048)
    rHidden = models.CharField(max_length=1024)
    rTimestamp = models.CharField(max_length=128)

    def __str__(self):
        return self.rTimestamp
