# Generated by Django 4.1.1 on 2023-02-09 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_infraforproject_project_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infraforproject',
            name='infra_content_type',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.RemoveField(
            model_name='rigforproject',
            name='rig',
        ),
        migrations.DeleteModel(
            name='InfraForProject',
        ),
        migrations.DeleteModel(
            name='RigForProject',
        ),
    ]