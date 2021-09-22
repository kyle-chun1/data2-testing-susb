from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Location)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Pricing)
admin.site.register(Category)


class LinkAdmin(admin.ModelAdmin):
    # fields = ['url','category']
    list_display = ('category','order','text')

admin.site.register(Link, LinkAdmin)
