# Generated by Django 4.1.1 on 2023-02-19 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_project_tax_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='opex',
            field=models.FloatField(default=0, verbose_name='Opex'),
        ),
        migrations.AddField(
            model_name='project',
            name='property_taxes',
            field=models.FloatField(default=0, verbose_name='Property Taxes'),
        ),
    ]
