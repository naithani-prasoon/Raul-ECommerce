from django.db import models
import stripe
from django.conf import settings
from django.contrib.auth.signals import user_logged_in


# Create your models here.

class UserDefaultAddress(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    shipping= models.ForeignKey("UserAddress", null=True, blank=True,on_delete=models.CASCADE, related_name='user_address_shipping_default+' )
    billing= models.ForeignKey("UserAddress", null=True, blank=True,on_delete=models.CASCADE, related_name='user_address_billing)default+' )

    def __unicode__(self):
        return str(self.user.username)


class UserAddressManager(models.Manager):
    def get_billing_addresses(self,user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)




stripe.api_key = settings.STRIPE_SECRET_KEY

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=120,null=True)
    lastname =  models.CharField(max_length=120,null=True)
    address = models.CharField(max_length=120,null=True)
    address2 = models.CharField(max_length=120,null=True)
    address3 = models.CharField(max_length=120,null=True)
    city = models.CharField(max_length=120,null=True)
    state = models.CharField(max_length=120,null=True)
    country = models.CharField(max_length=120,null=True)
    zipcode = models.CharField(max_length=120,null=True)
    phone = models.CharField(max_length=120,null=True)
    shipping = models.BooleanField(max_length=120,null=True)
    default = models.BooleanField(default=False)
    billing = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(max_length=120,null=True)
    updated = models.DateTimeField(max_length=120,null=True)

    def __str__(self):
        return self.get_address()


    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.address, self.city, self.state, self.country, self.zipcode)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-time_stamp']


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=127)

    def __str__(self):
        return str(self.stripe_id)

def get_or_create_stripe(sender, user, *args, **kwargs):
    try:
        user.userstripe.stripe_id
    except UserStripe.DoesNotExist:
        customer = stripe.Customer.create(
            email= user.email
        )
        new_user_stripe = UserStripe.objects.create(
            user=user,
            stripe_id = customer.id
        )
    except:
        pass

user_logged_in.connect(get_or_create_stripe)


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=120,null=True)
    lastname =  models.CharField(max_length=120,null=True)
    address = models.CharField(max_length=120,null=True)
    address2 = models.CharField(max_length=120,null=True)
    address3 = models.CharField(max_length=120,null=True)
    city = models.CharField(max_length=120,null=True)
    state = models.CharField(max_length=120,null=True)
    country = models.CharField(max_length=120,null=True)
    zipcode = models.CharField(max_length=120,null=True)
    phone = models.CharField(max_length=120,null=True)
    shipping = models.BooleanField(max_length=120,null=True)
    time_stamp = models.DateTimeField(max_length=120,null=True)
    updated = models.DateTimeField(max_length=120,null=True)

    def __str__(self):
        return self.get_address()


    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.address, self.city, self.state, self.country, self.zipcode)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-time_stamp']
