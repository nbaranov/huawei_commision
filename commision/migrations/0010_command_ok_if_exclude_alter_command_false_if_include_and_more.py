# Generated by Django 4.2 on 2023-07-05 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commision', '0009_alter_command_false_if_include_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='ok_if_exclude',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='command',
            name='false_if_include',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='command',
            name='ok_if_include',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
    ]