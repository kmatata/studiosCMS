# Generated by Django 4.1 on 2023-06-02 17:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("flats", "0009_rename_flat_flat_payments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="flat",
            name="payments",
        ),
    ]