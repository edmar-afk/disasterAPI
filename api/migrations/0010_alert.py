# Generated by Django 5.0.6 on 2024-08-07 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warning_text', models.TextField()),
                ('location', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
    ]
