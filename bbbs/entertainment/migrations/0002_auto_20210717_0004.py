# Generated by Django 3.2.5 on 2021-07-16 21:04

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='color',
            field=colorfield.fields.ColorField(choices=[('#F8D162', 'Жёлтый'), ('#8CDD94', 'Зелёный'), ('#FF8484', 'Розовый'), ('#C8D1FF', 'Голубой')], default='#FFFFFF', max_length=8, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='link',
            field=models.URLField(default=None, unique=True, verbose_name='Ссылка на фильм'),
            preserve_default=False,
        ),
    ]
