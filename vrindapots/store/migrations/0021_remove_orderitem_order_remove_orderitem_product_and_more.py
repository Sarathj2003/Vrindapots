# Generated by Django 5.1.1 on 2024-11-11 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]