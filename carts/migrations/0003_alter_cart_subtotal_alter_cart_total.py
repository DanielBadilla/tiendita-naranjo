# Generated by Django 5.1 on 2024-12-14 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
