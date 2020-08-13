from django.contrib import admin

# Register your models here.

from .models import Order, StripeInfo
class orderAdmin(admin.ModelAdmin):
    search_fields = ['user','Tracking_Status']
    list_display = ['user', 'final_total', 'order_pdf']
    list_filter =['user', 'Tracking_Status']
    readonly_fields = ['updated']
    class meta:
        model = Order

admin.site.register(Order,orderAdmin)
admin.site.register(StripeInfo)
