# Generated by Django 5.0.6 on 2024-07-01 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userDashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]