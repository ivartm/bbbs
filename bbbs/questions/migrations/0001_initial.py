# Generated by Django 3.2.5 on 2021-07-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название тега')),
                ('slug', models.SlugField(unique=True, verbose_name='Адрес тега')),
            ],
            options={
                'verbose_name': 'Тег (вопросы)',
                'verbose_name_plural': 'Теги (вопросы)',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, unique=True, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ на вопрос')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('tags', models.ManyToManyField(related_name='questions', to='questions.QuestionTag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ('-pub_date',),
            },
        ),
    ]
