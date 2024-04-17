# Generated by Django 4.2.8 on 2024-04-17 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSubscribes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.TextField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.provider')),
            ],
            options={
                'verbose_name': 'Заявка на подписку',
                'verbose_name_plural': 'Заявки на подписку',
            },
        ),
    ]