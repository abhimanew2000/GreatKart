# Generated by Django 4.2.3 on 2023-08-07 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0014_remove_address_email_remove_address_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='email',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='address',
            name='first_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='address',
            name='last_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(default=None, max_length=15),
        ),
    ]
