# Generated by Django 5.0.6 on 2024-06-26 16:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_generate_adminuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]