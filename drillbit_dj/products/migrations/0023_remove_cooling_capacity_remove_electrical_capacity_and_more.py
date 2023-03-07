# Generated by Django 4.1.1 on 2023-03-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_cooling_capacity_alter_electrical_capacity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooling',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='electrical',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='heatrejection',
            name='capacity',
        ),
        migrations.AddField(
            model_name='cooling',
            name='power_capacity',
            field=models.FloatField(default=None, null=True, verbose_name='Power Capacity'),
        ),
        migrations.AddField(
            model_name='electrical',
            name='power_capacity',
            field=models.FloatField(default=None, null=True, verbose_name='Power Capacity'),
        ),
        migrations.AddField(
            model_name='heatrejection',
            name='power_capacity',
            field=models.FloatField(default=None, null=True, verbose_name='Power Capacity'),
        ),
    ]