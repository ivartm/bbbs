# Generated by Django 3.2.3 on 2021-05-20 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('address', models.CharField(max_length=200)),
                ('contact', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('seats', models.IntegerField()),
                ('taken_seats', models.IntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='event', to='common.city')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'ordering': ['start_at'],
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='eventparticipant', to='afisha.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventparticipant', to=settings.AUTH_USER_MODEL)),
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
