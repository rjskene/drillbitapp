# Generated by Django 4.1.1 on 2023-02-22 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_projectstatement_frequency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectstatement',
            name='env',
        ),
        migrations.AlterField(
            model_name='projectstatement',
            name='frequency',
            field=models.CharField(choices=[('D', 'Daily'), ('M', 'Monthly'), ('Q', 'Quarterly'), ('A', 'Annually')], max_length=10, verbose_name='Frequency'),
        ),
    ]
