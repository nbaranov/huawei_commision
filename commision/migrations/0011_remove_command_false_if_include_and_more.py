# Generated by Django 4.2 on 2023-08-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commision', '0010_command_ok_if_exclude_alter_command_false_if_include_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='false_if_include',
        ),
        migrations.RemoveField(
            model_name='command',
            name='out_line_limit',
        ),
        migrations.AddField(
            model_name='command',
            name='false_comment',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='command',
            name='ok_if_exclude',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='command',
            name='ok_if_include',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
