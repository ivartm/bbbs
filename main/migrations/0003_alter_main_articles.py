# Generated by Django 3.2.4 on 2021-07-01 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0002_auto_20210629_2358'),
        ('main', '0002_main_articles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main',
            name='articles',
            field=models.ManyToManyField(to='entertainment.Article', verbose_name='Статьи'),
        ),
    ]