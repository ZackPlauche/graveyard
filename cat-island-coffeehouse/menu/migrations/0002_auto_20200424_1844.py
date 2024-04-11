# Generated by Django 3.0.5 on 2020-04-24 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.FloatField(blank=True, help_text='Enter the price in 0.00 format. Will be shown in USD.', null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='title',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
