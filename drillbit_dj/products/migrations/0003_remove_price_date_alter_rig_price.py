# Generated by Django 4.1.1 on 2023-01-29 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_rig_unique_together_alter_rig_generation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='date',
        ),
        migrations.AlterField(
            model_name='rig',
            name='price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='products.price'),
        ),
    ]