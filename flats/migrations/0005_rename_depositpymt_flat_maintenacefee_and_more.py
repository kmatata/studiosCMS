# Generated by Django 4.1 on 2023-06-01 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("authy", "0010_remove_paymentlog_deposit_and_more"),
        ("flats", "0004_flat_depositpymt_flat_unitpricemaintenance_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="flat",
            old_name="depositPymt",
            new_name="maintenaceFee",
        ),
        migrations.RenameField(
            model_name="flat",
            old_name="unitPrice",
            new_name="rentalFee",
        ),
        migrations.RenameField(
            model_name="flat",
            old_name="unitPriceMaintenance",
            new_name="threeMonthDeposit",
        ),
        migrations.RemoveField(
            model_name="flat",
            name="occupiedPeriod",
        ),
        migrations.RemoveField(
            model_name="flat",
            name="payment_status",
        ),
        migrations.RemoveField(
            model_name="flat",
            name="unitPriceSewage",
        ),
        migrations.RemoveField(
            model_name="flat",
            name="unitPriceWater",
        ),
        migrations.RemoveField(
            model_name="flat",
            name="vacantPeriod",
        ),
        migrations.AddField(
            model_name="flat",
            name="date",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="flat",
            name="depositPaid",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="flat",
            name="flat",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="flat",
                to="authy.paymentlog",
            ),
        ),
        migrations.CreateModel(
            name="Water",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unitPrice",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("quantity", models.PositiveBigIntegerField()),
                ("date", models.DateTimeField(auto_now=True)),
                (
                    "payments",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="water",
                        to="authy.paymentlog",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sewage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unitPrice",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("quantity", models.PositiveBigIntegerField()),
                ("date", models.DateTimeField(auto_now=True)),
                (
                    "payments",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sewage",
                        to="authy.paymentlog",
                    ),
                ),
            ],
        ),
    ]
