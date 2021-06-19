# Generated by Django 3.2.4 on 2021-06-18 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rights', '0003_auto_20210612_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='right',
            name='tag',
        ),
        migrations.AddField(
            model_name='right',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='righttags', to='rights.RightTag'),
        ),
    ]