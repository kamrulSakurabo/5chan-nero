# Generated by Django 4.2.2 on 2023-07-04 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gochan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='searchPlace',
            field=models.CharField(default='5ch(2ch)', max_length=255),
        ),
    ]
