# Generated by Django 3.0.5 on 2020-04-25 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20200424_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='short_description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
