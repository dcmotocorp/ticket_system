# Generated by Django 3.2.4 on 2022-03-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='updated_worklog',
            field=models.IntegerField(),
        ),
    ]