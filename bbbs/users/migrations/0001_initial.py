# Generated by Django 3.2.5 on 2021-07-15 19:05

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
            name='Curator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('gender', models.CharField(choices=[('female', 'женский'), ('male', 'мужской')], max_length=10, verbose_name='Пол')),
                ('email', models.EmailField(max_length=25)),
            ],
            options={
                'verbose_name': 'Куратор',
                'verbose_name_plural': 'Кураторы',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Наставник', 'Наставник'), ('Модератор(региональный)', 'Модератор(региональный)'), ('Модератор(общий)', 'Модератор(общий)'), ('Администратор', 'Администратор')], default='Наставник', max_length=25, verbose_name='Роль')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='common.city', verbose_name='Город')),
                ('curator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='users.curator', verbose_name='Куратор')),
                ('region', models.ManyToManyField(blank=True, related_name='region', related_query_name='region', to='common.City', verbose_name='Обслуживаемые города')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
            },
        ),
    ]
