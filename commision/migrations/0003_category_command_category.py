# Generated by Django 4.2 on 2023-06-02 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commision', '0002_command_for_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='command',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='commision.category'),
        ),
    ]
