# Generated by Django 4.1.1 on 2023-01-29 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_new_price_rig_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Price',
        ),
    ]