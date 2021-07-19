from django.db import models

# from Pricing.models import Location, ProductType

# Create your models here.
# class Movement(models.Model):
#     location_choices = [('I','IRC'),('T','TRMC'),('7','700')]  # COPIED + HARCODED FROM PRICING
#     od_choices = [('D','Donations'),('O','Overflow'),('P','Processing'),('S','Salesfloor')]
#     origin = models.CharField(max_length=1, choices=od_choices)
#     destination = models.CharField(max_length=1, choices=od_choices)
#     quantity = models.DecimalField(max_digits=4,decimal_places=2)
#     staff_id = models.CharField(max_length=32)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     origin_location = models.CharField(max_length=1, choices=location_choices)
#     destination_location = models.CharField(max_length=1, choices=location_choices)
#     product_type = models.ForeignKey('pricing.ProductType', on_delete=models.PROTECT)
