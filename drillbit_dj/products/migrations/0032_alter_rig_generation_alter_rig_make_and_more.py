# Generated by Django 4.1.1 on 2023-04-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_alter_rig_make_alter_rig_manufacturer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rig',
            name='generation',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='rig',
            name='make',
            field=models.CharField(default='', max_length=100, verbose_name='Make'),
        ),
        migrations.AlterField(
            model_name='rig',
            name='manufacturer',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='rig',
            name='model',
            field=models.CharField(default='', max_length=100),
        ),
    ]