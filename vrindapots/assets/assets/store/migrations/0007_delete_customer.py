# Generated by Django 5.1.1 on 2024-10-09 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_category_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
