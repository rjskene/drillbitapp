# Generated by Django 4.1.1 on 2023-03-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_heatrejection_design_dry_bulb'),
    ]

    operations = [
        migrations.AddField(
            model_name='rejectioncurve',
            name='raw',
            field=models.JSONField(default=dict),
        ),
    ]
