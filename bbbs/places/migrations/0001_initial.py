# Generated by Django 3.2.5 on 2021-07-15 19:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Тег (места: куда пойти?)',
                'verbose_name_plural': 'Теги (места: куда пойти?)',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen', models.BooleanField(default=False, verbose_name='Выбор наставника')),
                ('published', models.BooleanField(default=False, verbose_name='Опубликован')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мальчик'), ('F', 'Девочка')], max_length=1, null=True, verbose_name='Пол')),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(40)], verbose_name='Возраст')),
                ('activity_type', models.PositiveSmallIntegerField(choices=[(0, 'Активный'), (1, 'Развлекательный'), (2, 'Познавательный')], verbose_name='Тип отдыха')),
                ('description', models.TextField(help_text='Поделитесь впечатлениями о проведенном времени', max_length=2000, verbose_name='Комментарий')),
                ('link', models.URLField(blank=True, help_text='Введите адрес сайта', null=True, verbose_name='Сайт')),
                ('image_url', models.ImageField(help_text='Добавить фото', upload_to='places/', verbose_name='Фото')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places', to='common.city', verbose_name='Город')),
                ('tags', models.ManyToManyField(related_name='places', to='places.PlaceTag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Место - куда пойти?',
                'verbose_name_plural': 'Места - куда пойти?',
                'ordering': ('id',),
            },
        ),
        migrations.AddConstraint(
            model_name='place',
            constraint=models.UniqueConstraint(fields=('title', 'address', 'city'), name='unique_place_for_city'),
        ),
    ]
