# Generated by Django 3.0.7 on 2020-07-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Raul', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Plates', 'Plates'), ('Pot', 'Pot'), ('Flowers', 'Flowers'), ('Table', 'Table')], default='Plates', max_length=128),
        ),
    ]
