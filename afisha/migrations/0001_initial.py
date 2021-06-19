# Generated by Django 3.2.3 on 2021-06-08 12:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('contact', models.CharField(max_length=200, verbose_name='Контакт')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Дополнительная информация')),
                ('startAt', models.DateTimeField(verbose_name='Начало')),
                ('endAt', models.DateTimeField(verbose_name='Окончание')),
                ('seats', models.PositiveIntegerField(verbose_name='Свободные места')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='events', to='common.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
                'ordering': ['startAt'],
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='event_participants', to='afisha.event', verbose_name='Мероприятие')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_participants', to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
                'ordering': ['-event'],
            },
        ),
        migrations.AddConstraint(
            model_name='eventparticipant',
            constraint=models.UniqueConstraint(fields=('user', 'event'), name='unique_participant'),
        ),
    ]
