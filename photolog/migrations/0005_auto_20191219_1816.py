# Generated by Django 3.0.1 on 2019-12-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photolog', '0004_photoobject_shortdesc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalog',
            options={'ordering': ['sort'], 'verbose_name': 'Каталог', 'verbose_name_plural': 'Каталоги'},
        ),
        migrations.AlterModelOptions(
            name='images',
            options={'ordering': ['sort'], 'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterModelOptions(
            name='photoobject',
            options={'ordering': ['sort'], 'verbose_name': 'Фотообъект', 'verbose_name_plural': 'Фотообъекты'},
        ),
        migrations.AddField(
            model_name='catalog',
            name='sort',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Порядок'),
        ),
        migrations.AddField(
            model_name='images',
            name='sort',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Порядок'),
        ),
        migrations.AddField(
            model_name='photoobject',
            name='sort',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Порядок'),
        ),
    ]