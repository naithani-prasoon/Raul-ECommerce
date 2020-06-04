from django.contrib import admin
from .models import product

# Register your models here.

class productAdmin(admin.ModelAdmin):
        search_fields = ['title','description']
        list_display = ['title', 'price', 'active', 'updated', 'description']
        list_editable = ['price','active']
        list_filter =['active', 'price']
        readonly_fields = ['updated', 'time_stamp']
        prepopulated_fields = {"slug": ("title",)}
        class meta:
            model = product
admin.site.register(product,productAdmin)

