# Generated by Django 5.1.1 on 2024-10-25 19:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_profile_pincode_profile_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number must be exactly 10 digits', regex='^\\d{10}$')]),
        ),
    ]
