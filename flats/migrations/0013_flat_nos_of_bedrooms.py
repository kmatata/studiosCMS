# Generated by Django 4.1 on 2023-06-19 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flats", "0012_flat_sewageunitcost_flat_waterunitcost"),
    ]

    operations = [
        migrations.AddField(
            model_name="flat",
            name="nos_of_bedrooms",
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]