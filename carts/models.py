from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

from Raul.models import product
User = get_user_model()

class CartItem(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', null=True, blank=True,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True)
    line_total = models.DecimalField(default=1000.00, max_digits=1000, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
            return (self.product.title)



class Cart(models.Model):
    cart_items = models.ManyToManyField(CartItem,related_name="CARTITEMS")
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    pennies_total = models.DecimalField(max_digits=100000000, decimal_places=0, default=0)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)



