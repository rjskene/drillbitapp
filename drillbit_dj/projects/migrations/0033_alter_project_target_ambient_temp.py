# Generated by Django 4.1.1 on 2023-04-02 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_alter_projectstatement_roi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='target_ambient_temp',
            field=models.JSONField(default=dict, null=True, verbose_name='Target Ambient Temperature'),
        ),
    ]
