# Generated by Django 4.1.1 on 2023-04-02 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0033_alter_project_target_ambient_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='infraforproject',
            name='price',
            field=models.FloatField(null=True, verbose_name='Price'),
        ),
        migrations.AddField(
            model_name='rigforproject',
            name='price',
            field=models.FloatField(null=True, verbose_name='Price'),
        ),
    ]
