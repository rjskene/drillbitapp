# Generated by Django 4.1.1 on 2023-04-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_alter_rig_generation_alter_rig_make_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rig',
            name='generation',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rig',
            name='make',
            field=models.CharField(max_length=100, null=True, verbose_name='Make'),
        ),
        migrations.AlterField(
            model_name='rig',
            name='manufacturer',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rig',
            name='model',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
