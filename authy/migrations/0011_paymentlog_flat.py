# Generated by Django 4.1 on 2023-06-02 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("flats", "0010_remove_flat_payments"),
        ("authy", "0010_remove_paymentlog_deposit_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentlog",
            name="flat",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="flat",
                to="flats.flat",
            ),
        ),
    ]
