# Generated by Django 5.1.1 on 2024-11-16 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigIntegerField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
