# Generated by Django 4.2.8 on 2024-01-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='total_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
