# Generated by Django 5.1.1 on 2024-11-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_remove_coupon_minimum_order_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='final_price',
        ),
        migrations.AddField(
            model_name='order',
            name='coupon_applied',
            field=models.BooleanField(default=False),
        ),
    ]
