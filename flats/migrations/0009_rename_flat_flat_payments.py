# Generated by Django 4.1 on 2023-06-02 17:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("flats", "0008_sewage_flat_water_flat_alter_flat_flat"),
    ]

    operations = [
        migrations.RenameField(
            model_name="flat",
            old_name="flat",
            new_name="payments",
        ),
    ]
