# Generated by Django 5.1.1 on 2024-11-28 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_profile_is_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='from_flag',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]