# Generated by Django 3.0.5 on 2025-03-02 11:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20250227_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
