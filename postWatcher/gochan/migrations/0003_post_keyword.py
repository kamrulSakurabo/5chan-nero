# Generated by Django 4.2.2 on 2023-07-04 08:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gochan', '0002_alter_post_searchplace'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='keyword',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
