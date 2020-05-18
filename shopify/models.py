from django.db import models

#NEED TO KILL THIS
# class AceInventory(models.Model):
#     Index = models.IntegerField(primary_key=True)
#     ItemCode = models.CharField(max_length=64)
#     Location = models.CharField(max_length=64)
#     Department = models.CharField(max_length=64)
#     Title = models.CharField(max_length=1024)
#     Upc = models.CharField(max_length=64)
#     Qoh = models.IntegerField()
#     Mpn = models.CharField(max_length=64)
#     Retail = models.DecimalField(max_digits=8, decimal_places=2)
#     Status = models.CharField(max_length=64)



class AceInventoryList(models.Model):
    Index = models.IntegerField(primary_key=True)
    ItemCode = models.CharField(max_length=64)
    Location = models.CharField(max_length=64)
    Department = models.CharField(max_length=64)
    Title = models.CharField(max_length=1024)
    Upc = models.CharField(max_length=64)
    Qoh = models.IntegerField()
    Mpn = models.CharField(max_length=64)
    Retail = models.DecimalField(max_digits=8, decimal_places=2)
    Status = models.CharField(max_length=64)
