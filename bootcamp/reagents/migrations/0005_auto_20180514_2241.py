# Generated by Django 2.0.4 on 2018-05-14 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reagents', '0004_auto_20180510_2312'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CellBiologicContent',
            new_name='CellContent',
        ),
    ]
