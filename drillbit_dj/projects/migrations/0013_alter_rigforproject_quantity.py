# Generated by Django 4.1.1 on 2023-02-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_alter_project_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rigforproject',
            name='quantity',
            field=models.FloatField(null=True, verbose_name='Quantity'),
        ),
    ]
