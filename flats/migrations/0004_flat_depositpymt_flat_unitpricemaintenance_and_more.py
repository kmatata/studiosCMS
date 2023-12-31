# Generated by Django 4.1 on 2023-05-31 00:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flats", "0003_flat_unitprice"),
    ]

    operations = [
        migrations.AddField(
            model_name="flat",
            name="depositPymt",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="flat",
            name="unitPriceMaintenance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="flat",
            name="unitPriceSewage",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="flat",
            name="unitPriceWater",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
