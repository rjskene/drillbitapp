# Generated by Django 4.1.1 on 2023-02-21 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_alter_projectstatement_sim'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstatement',
            name='frequency',
            field=models.CharField(choices=[('BLOCK', 'Block'), ('D', 'Daily'), ('M', 'Monthly'), ('Q', 'Quarterly'), ('A', 'Annually')], default='BLOCK', max_length=10, verbose_name='Frequency'),
            preserve_default=False,
        ),
    ]
