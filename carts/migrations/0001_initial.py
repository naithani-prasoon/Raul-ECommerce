# Generated by Django 3.0.7 on 2020-07-30 02:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Raul', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('pennies_total', models.DecimalField(decimal_places=0, default=0, max_digits=100000000)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, null=True)),
                ('line_total', models.DecimalField(decimal_places=2, default=1000.0, max_digits=1000)),
                ('notes', models.TextField(blank=True, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Raul.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variation', models.ManyToManyField(blank=True, to='Raul.Variation')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_items',
            field=models.ManyToManyField(related_name='CARTITEMS', to='carts.CartItem'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
