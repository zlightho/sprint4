# Generated by Django 2.2.1 on 2021-12-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20211202_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
