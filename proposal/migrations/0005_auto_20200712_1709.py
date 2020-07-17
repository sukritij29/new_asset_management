# Generated by Django 3.0.8 on 2020-07-12 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0004_auto_20200711_1721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposal',
            old_name='amount',
            new_name='proposed_amount',
        ),
        migrations.AddField(
            model_name='documentation',
            name='amount',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]