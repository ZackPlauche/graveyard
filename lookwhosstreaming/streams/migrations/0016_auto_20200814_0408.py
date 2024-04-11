# Generated by Django 3.0.6 on 2020-08-14 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0015_auto_20200725_2051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['streamer']},
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(default='TEMP', max_length=100, verbose_name='Account Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stream',
            name='shady',
            field=models.BooleanField(default=False, verbose_name='Manual'),
        ),
    ]