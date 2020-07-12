from django.contrib import admin

# Register your models here.

from .models import Order, StripeInfo

admin.site.register(Order)
admin.site.register(StripeInfo)
