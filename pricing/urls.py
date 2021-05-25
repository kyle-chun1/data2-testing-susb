from django.urls import path

from pricing.views import pricing_portal, pricing_submit, my_pricing_table, raw, stats

app_name='pricing'

urlpatterns = [
    path('portal/<slug:location>/', pricing_portal, name='portal'),
    path('raw/<slug:location>/', raw, name='raw'),
    path('stats/<slug:location>/', stats, name='stats'),
    path('submit/', pricing_submit, name='submit'),

    path('my_pricing_table/', my_pricing_table, name='my_pricing_table'),
    # USED FOR RON / MANUALLY PRICING OUT BULK PRICED ITEMS
    # path('temp_barcode/', temp_barcode, name='temp_barcode'),
]
