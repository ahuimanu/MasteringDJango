# Generated by Django 3.2 on 2021-04-22 00:00

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20201221_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('myclubuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.myclubuser')),
                ('date_joined', models.DateTimeField()),
            ],
            bases=('events.myclubuser',),
        ),
        migrations.AlterModelManagers(
            name='venue',
            managers=[
                ('venues', django.db.models.manager.Manager()),
            ],
        ),
    ]
