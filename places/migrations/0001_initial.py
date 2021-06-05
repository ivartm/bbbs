# Generated by Django 3.2.3 on 2021-06-05 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen', models.BooleanField(default=False, verbose_name='Выбор наставника')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мальчик'), ('F', 'Девочка')], max_length=1, null=True, verbose_name='Пол')),
                ('age', models.PositiveSmallIntegerField(verbose_name='Возраст')),
                ('activity_type', models.PositiveSmallIntegerField(choices=[(0, 'Активный'), (1, 'Развлекательный'), (2, 'Познавательный')], verbose_name='Тип отдыха')),
                ('description', models.TextField(help_text='Поделитесь впечатлениями о проведенном времени', verbose_name='Комментарий')),
                ('link', models.URLField(blank=True, help_text='Введите адрес сайта', null=True, verbose_name='Сайт')),
                ('imageUrl', models.ImageField(blank=True, help_text='Добавить фото', null=True, upload_to='places/', verbose_name='Фото')),
                ('tag', models.ManyToManyField(to='common.Tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Место - куда пойти?',
                'verbose_name_plural': 'Места - куда пойти?',
            },
        ),
    ]
