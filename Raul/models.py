from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name



options = Category.objects.all().values_list('name','name')
arr = []
for i in options:
    arr.append(i)


options2 = Section.objects.all().values_list('name','name')
arr2 = []
for i in options2:
    arr2.append(i)


class product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    image = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=128, choices=arr)
    section = models.CharField(max_length=128, choices=arr2)
    slug = models.SlugField(null = True)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    imageFound = models.BooleanField(default=False)
    Overweight = models.BooleanField(default=False)
    SuperOverweight = models.BooleanField(default=False)

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

class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)
    def sizes(self):
        return self.all().filter(category= 'size')
    def colors(self):
        return self.all().filter(category= 'color')

VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package'),
    )

class Variation(models.Model):
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default="size")
    title= models.CharField(max_length=120)
    image = models.ImageField(blank=True, null=True)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=100)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    objects = VariationManager()

    def __str__(self):
        return self.product.title

class FeatuedProducts(models.Model):
    product = models.ForeignKey(product, on_delete=models.PROTECT)

    def  __str__(self):
        return self.product.title






