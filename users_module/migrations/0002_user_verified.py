# Generated by Django 3.0.8 on 2020-07-12 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
