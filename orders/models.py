from django.contrib.auth import get_user_model
from django.db import models
from users.views import UserAddress
from decimal import Decimal

# Create your models here.
from carts.models import Cart
from users.models import UserAddress, BillingAddress
User = get_user_model()
User2 = get_user_model()


STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)

SHIPPING_CHOICES = (
    ("Processing", "Processing"),
    ("Shipped", "Shipped"),
    ("Cancelled", "Cancelled"),
)

class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(BillingAddress, related_name= "billing_address", blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(UserAddress,related_name= "shipping_address", blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    sub_total = models.DecimalField(default=1000.00, max_digits=1000, decimal_places=2)
    tax_total = models.DecimalField(default=1000.00, max_digits=1000, decimal_places=2)
    final_total = models.DecimalField(default=1000.00, max_digits=1000, decimal_places=2)
    Tracking_Status = models.CharField(max_length=120, choices=SHIPPING_CHOICES, default="Processing",blank=True, null=True)
    Shipping = models.DecimalField(max_length=120,default=9.00,blank=True,null=True,max_digits=1000, decimal_places=2)
    Tracking_Number = models.CharField(max_length=120,blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    order_pdf = models.FileField(blank=True,null=True)

    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.order_id

    def get_final_amount(self):
        instance = Order.objects.get(id =self.id)
        two_places = Decimal(10) ** -2
        instance.tax_total = Decimal(Decimal("0.08") * Decimal(self.sub_total)).quantize(two_places)
        instance.final_total = Decimal(self.sub_total) + Decimal(instance.tax_total)
        instance.save()

class StripeInfo(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    last4 = models.CharField(max_length=120, unique=True)
    exp =  models.CharField(max_length=120, unique=True)
    card_id = models.CharField(max_length=120, unique=True)


