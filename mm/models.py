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

    def __all__(self):
        return {
            'rName' : self.rName,
            'rDate' : self.rDate,
            'rTrips' : self.rTrips,
            'rMode' : self.rMode,
            'rOrigin' : self.rOrigin,
            'rOriginLocation' : self.rOriginLocation,
            'rDestination' : self.rDestination,
            'rDestinationLocation' : self.rDestinationLocation,
            'rMaterial' : self.rMaterial,
            'rHidden' : self.rHidden,
            'rTimestamp' : self.rTimestamp,
            }

class ExpandedMaterialMovement(models.Model):
        eName = models.CharField(max_length=128)
        eDate = models.DateField()
        eMode = models.CharField(max_length=128)
        eTrips = models.CharField(max_length=128)
        eOrigin = models.CharField(max_length=128)
        eOriginLocation = models.CharField(max_length=128)
        eDestination = models.CharField(max_length=128)
        eDestinationLocation = models.CharField(max_length=128)
        eTimestamp = models.CharField(max_length=128)
        eMaterial = models.CharField(max_length=128)
        ePallets = models.CharField(max_length=128)
        eTripID = models.CharField(max_length=128)

        # REMOVED rMaterial :)
        # REMOVED rHidden :)
        # ADDED : ePallets + eMaterial + eTripID(SHA256 HASH)
