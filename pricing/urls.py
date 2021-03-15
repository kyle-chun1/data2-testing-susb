from django.urls import path


from pricing.views import tester2

urlpatterns = [
    path('tester2/', tester2, name='tester2')
]
