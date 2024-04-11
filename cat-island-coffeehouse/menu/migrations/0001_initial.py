# Generated by Django 3.0.5 on 2020-04-24 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('order', models.PositiveIntegerField(null=True)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, help_text='Enter the price in $00.00 format.', null=True)),
                ('display', models.BooleanField(default=True)),
                ('favorite', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.MenuCategory')),
            ],
        ),
    ]
