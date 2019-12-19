# Generated by Django 3.0.1 on 2019-12-19 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20191219_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardmodel',
            name='sort',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Порядок'),
        ),
        migrations.AddField(
            model_name='standardmodel',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано')], default='draft', max_length=10, verbose_name='Статус'),
        ),
    ]