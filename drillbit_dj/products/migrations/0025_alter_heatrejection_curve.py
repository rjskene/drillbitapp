# Generated by Django 4.1.1 on 2023-03-03 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_remove_cooling_power_capacity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heatrejection',
            name='curve',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.rejectioncurve'),
        ),
    ]
