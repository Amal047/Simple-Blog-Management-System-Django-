# Generated by Django 5.2 on 2025-05-06 14:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_otpverification_delete_emailotp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpverification',
            name='expiry_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
