# Generated by Django 3.0.5 on 2020-04-24 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20200421_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='category',
        ),
        migrations.DeleteModel(
            name='MenuCategory',
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
    ]
