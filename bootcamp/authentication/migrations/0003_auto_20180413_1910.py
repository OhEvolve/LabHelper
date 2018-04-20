# Generated by Django 2.0.4 on 2018-04-13 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_profile_passcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job_title',
            field=models.CharField(blank=True, choices=[('undergrad', 'Undergraduate Student'), ('_graduate', 'Graduate Student'), ('_research', 'Research Scientist'), ('principle', 'Principle Investigator')], max_length=50, null=True),
        ),
    ]
