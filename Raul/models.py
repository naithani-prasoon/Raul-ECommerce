from django.db import models

# Create your models here.

class product(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    images = models.FileField(upload_to='raul_project/Raul/static.Raul/Images', null= True)

    slug = models.SlugField(null = True)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title





