# Generated by Django 4.1 on 2023-06-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authy", "0012_paymentlog_sewage_paymentlog_water"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentlog",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
