# Generated by Django 4.1.1 on 2023-02-09 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rigforproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rig', to='projects.project'),
        ),
    ]
