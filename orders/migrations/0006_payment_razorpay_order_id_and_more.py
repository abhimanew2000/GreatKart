# Generated by Django 4.2.3 on 2023-08-13 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_address_line_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
