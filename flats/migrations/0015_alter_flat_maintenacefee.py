# Generated by Django 4.1 on 2023-07-03 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flats", "0014_alter_sewage_unitprice_alter_water_unitprice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flat",
            name="maintenaceFee",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]