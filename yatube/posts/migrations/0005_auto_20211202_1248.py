# Generated by Django 2.2.1 on 2021-12-02 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_group_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='group',
            name='title',
        ),
    ]