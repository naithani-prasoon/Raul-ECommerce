from django.contrib import admin
from .models import product, productimage , Category, Variation, Section

# Register your models here.

class productAdmin(admin.ModelAdmin):
        search_fields = ['title','description', 'category']
        list_display = ['title', 'price', 'active', 'updated', 'description','category']
        list_editable = ['price','active']
        list_filter =['active', 'price', 'category']
        readonly_fields = ['updated', 'time_stamp']
        prepopulated_fields = {"slug": ("title",)}
        class meta:
            model = product
admin.site.register(product,productAdmin)
admin.site.register(productimage)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Variation)



