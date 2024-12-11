# Generated by Django 5.1.1 on 2024-10-25 19:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_profile_address_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pincode',
            field=models.CharField(max_length=6, null=True, validators=[django.core.validators.RegexValidator(code='invalid_pincode', message='Pincode must be exactly 6 digits', regex='^\\d{6}$')]),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'), ('Delhi', 'Delhi'), ('Chandigarh', 'Chandigarh'), ('Puducherry', 'Puducherry'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Ladakh', 'Ladakh')], max_length=50, null=True),
        ),
    ]