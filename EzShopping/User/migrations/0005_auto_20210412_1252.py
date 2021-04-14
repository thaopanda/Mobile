# Generated by Django 3.1.1 on 2021-04-12 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_auto_20210411_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='image',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='followed',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
