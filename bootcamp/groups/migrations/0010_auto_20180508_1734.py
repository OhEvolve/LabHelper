# Generated by Django 2.0.5 on 2018-05-08 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0009_auto_20180508_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Group'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]