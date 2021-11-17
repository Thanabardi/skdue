# Generated by Django 3.2.8 on 2021-11-16 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skdue_calendar', '0008_auto_20211110_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='theme_name',
            field=models.CharField(default='theme-1', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersetting',
            name='theme_type',
            field=models.CharField(default='light', max_length=32),
            preserve_default=False,
        ),
    ]
