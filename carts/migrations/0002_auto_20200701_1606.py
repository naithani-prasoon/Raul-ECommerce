# Generated by Django 3.0.7 on 2020-07-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Raul', '0002_auto_20200701_1606'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variation',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, null=True, to='Raul.Variation'),
        ),
    ]
