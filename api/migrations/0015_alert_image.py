# Generated by Django 5.0.6 on 2024-10-03 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='alerts/'),
        ),
    ]
