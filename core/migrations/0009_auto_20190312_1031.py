# Generated by Django 2.1.4 on 2019-03-12 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190310_1750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standardmodel',
            old_name='type_case',
            new_name='prod_type',
        ),
    ]
