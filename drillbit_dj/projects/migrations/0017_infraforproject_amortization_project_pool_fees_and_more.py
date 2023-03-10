# Generated by Django 4.1.1 on 2023-02-15 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_alter_projects_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='infraforproject',
            name='amortization',
            field=models.FloatField(default=60, verbose_name='Amortization'),
        ),
        migrations.AddField(
            model_name='project',
            name='pool_fees',
            field=models.FloatField(default=0, verbose_name='Pool Fees'),
        ),
        migrations.AddField(
            model_name='rigforproject',
            name='amortization',
            field=models.FloatField(default=60, verbose_name='Amortization'),
        ),
    ]
