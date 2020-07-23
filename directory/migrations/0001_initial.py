# Generated by Django 3.0.7 on 2020-07-23 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('action', models.CharField(max_length=5)),
                ('path', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Erased',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('action', models.CharField(max_length=5)),
                ('path', models.CharField(max_length=50)),
            ],
        ),
    ]
