# Generated by Django 4.2.3 on 2023-07-20 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0005_user_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
