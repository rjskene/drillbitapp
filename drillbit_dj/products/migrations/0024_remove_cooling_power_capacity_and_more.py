# Generated by Django 4.1.1 on 2023-03-03 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_remove_cooling_capacity_remove_electrical_capacity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooling',
            name='power_capacity',
        ),
        migrations.RemoveField(
            model_name='electrical',
            name='power_capacity',
        ),
        migrations.RemoveField(
            model_name='heatrejection',
            name='power_capacity',
        ),
        migrations.AddField(
            model_name='cooling',
            name='capacity',
            field=models.FloatField(default=None, null=True, verbose_name='Power Capacity'),
        ),
        migrations.AddField(
            model_name='electrical',
            name='capacity',
            field=models.FloatField(default=None, null=True, verbose_name='Power Capacity'),
        ),
        migrations.AddField(
            model_name='heatrejection',
            name='capacity',
            field=models.FloatField(default=None, null=True, verbose_name='Power Capacity'),
        ),
    ]
