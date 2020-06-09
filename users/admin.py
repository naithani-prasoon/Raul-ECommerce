from django.contrib import admin
from .models import UserStripe, UserAddress

# Register your models here.
admin.site.register(UserStripe)
admin.site.register(UserAddress)
