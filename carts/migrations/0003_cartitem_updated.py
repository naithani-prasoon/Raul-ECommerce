# Generated by Django 3.0.6 on 2020-06-07 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20200607_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]