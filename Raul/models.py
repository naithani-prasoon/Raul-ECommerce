from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name




options = Category.objects.all().values_list('name','name')
arr = []
for i in options:
    arr.append(i)


class product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    image = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=128, default="Plates", choices=arr)
    slug = models.SlugField(null = True)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class productimage(models.Model):
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    image=models.ImageField()
    active = models.BooleanField(default=True)
    thumbnail = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.title






