from django.db import models

# Create your models here.

from Raul.models import product

class CartItem(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.products.title



class Cart(models.Model):
    items = models.ManyToManyField(CartItem, null=True,blank=True)
    products = models.ManyToManyField(product, null= True, blank= True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=1.00)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "Cart id: %s" %(self.id)



