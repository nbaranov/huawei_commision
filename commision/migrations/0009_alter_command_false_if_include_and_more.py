# Generated by Django 4.2 on 2023-06-27 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commision', '0008_rename_check_exclude_command_false_if_include_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='false_if_include',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='command',
            name='ok_if_include',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]