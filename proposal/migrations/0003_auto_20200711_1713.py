# Generated by Django 3.0.8 on 2020-07-11 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0002_auto_20200711_1212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposal',
            old_name='emails',
            new_name='email',
        ),
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('vendor_id', models.AutoField(primary_key=True, serialize=False)),
                ('email_address', models.CharField(blank=True, max_length=150)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendors', to='proposal.Proposal')),
            ],
        ),
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('link', models.URLField()),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentation', to='proposal.Proposal')),
            ],
        ),
    ]