# Generated by Django 5.2.1 on 2025-05-24 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travio_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tourpackage',
            name='destinations',
        ),
        migrations.AddField(
            model_name='tourpackage',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tourpackage',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
