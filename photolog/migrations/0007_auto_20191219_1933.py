# Generated by Django 3.0.1 on 2019-12-19 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photolog', '0006_auto_20191219_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано')], default='published', max_length=10, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='photoobject',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано')], default='published', max_length=10, verbose_name='Статус'),
        ),
    ]
