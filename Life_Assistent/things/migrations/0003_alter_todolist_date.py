# Generated by Django 4.2.7 on 2023-12-01 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0002_remove_todolist_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
