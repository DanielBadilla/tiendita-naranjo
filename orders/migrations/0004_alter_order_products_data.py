# Generated by Django 5.1 on 2024-12-16 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_products_data_alter_order_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products_data',
            field=models.JSONField(default=dict),
        ),
    ]
