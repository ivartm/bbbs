# Generated by Django 3.2.5 on 2021-07-08 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('story', '0002_auto_20210706_1900'),
        ('entertainment', '0001_initial'),
        ('questions', '0001_initial'),
        ('places', '0007_merge_0002_alter_place_tags_0006_alter_place_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articles', models.ManyToManyField(to='entertainment.Article', verbose_name='Статьи')),
                ('history', models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='story.story', verbose_name='История')),
                ('movies', models.ManyToManyField(to='entertainment.Movie', verbose_name='Фильмы')),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='places.place', verbose_name='Место - куда пойти?')),
                ('questions', models.ManyToManyField(to='questions.Question', verbose_name='Вопросы')),
                ('video', models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='entertainment.video', verbose_name='Видео')),
            ],
            options={
                'verbose_name': 'Главная страница',
                'verbose_name_plural': 'Главная страница',
            },
        ),
    ]
