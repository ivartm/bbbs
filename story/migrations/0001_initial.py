# Generated by Django 3.2.5 on 2021-07-04 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Загрузите фото', upload_to='stories/', verbose_name='Фото')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Название истории')),
                ('beginningOfFriendship', models.DateTimeField(verbose_name='Дата начала дружбы')),
                ('prolog', models.TextField(verbose_name='Пролог')),
                ('text', models.TextField(verbose_name='Текст истории')),
                ('pubDate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'Истории',
                'ordering': ('-beginningOfFriendship',),
            },
        ),
        migrations.CreateModel(
            name='StoryImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='stories/')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storyimages', to='story.story')),
            ],
        ),
    ]