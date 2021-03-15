from django.db import models

# Create your models here.
class Location(models.Model):
    location_choices = [('I','IRC'),('T','TRMC')]
    location = models.CharField(max_length=1, choices=location_choices)
    text = models.TextField(default='')
    shopify_location_id = models.CharField(max_length=16)
    def __str__(self):
        return self.location

class ProductType(models.Model):
    product_type = models.CharField(max_length=64)
    def __str__(self):
        return self.product_type

class Product(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    classifier_choices = [('U','Unit'),('W','White'),('Y','Yellow'),('R','Red'),('O','Orange'),('B','Blue'),('G','Green'),('L','Lavender')]
    classifier = models.CharField(max_length=1, choices = classifier_choices)
    code = models.CharField(max_length=3, unique=True)
    shopify_handle = models.CharField(max_length=5)
    def __str__(self):
        return self.shopify_handle

class Variant(models.Model):   #PROXY FOR BARCODE / SKU (Can be referenced!)
    variant = models.CharField(max_length=16)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    def __str__(self):
        return self.variant

class Pricing(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    staff_id = models.CharField(max_length=16)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.staff_id
