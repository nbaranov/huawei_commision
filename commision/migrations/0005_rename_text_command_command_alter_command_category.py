# Generated by Django 4.2 on 2023-06-02 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commision', '0004_alter_command_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='command',
            old_name='text',
            new_name='command',
        ),
        migrations.AlterField(
            model_name='command',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='commision.category'),
        ),
    ]