# Generated by Django 3.2.5 on 2021-08-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_hit',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
