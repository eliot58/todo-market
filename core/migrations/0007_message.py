# Generated by Django 4.2.8 on 2024-06-27 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_buyer_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_provider', models.BooleanField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='chat')),
                ('content', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.order')),
            ],
        ),
    ]
