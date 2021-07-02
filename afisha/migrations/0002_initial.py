# Generated by Django 3.2.4 on 2021-07-01 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('afisha', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='events', to='common.city', verbose_name='Город'),
        ),
        migrations.AddConstraint(
            model_name='eventparticipant',
            constraint=models.UniqueConstraint(fields=('user', 'event'), name='unique_participant'),
        ),
    ]