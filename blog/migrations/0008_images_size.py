# Generated by Django 2.1.7 on 2019-04-20 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20190313_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='size',
            field=models.SmallIntegerField(choices=[('180', 180), ('300', 300), ('600', 600), ('800', 800)], default='300'),
        ),
    ]
