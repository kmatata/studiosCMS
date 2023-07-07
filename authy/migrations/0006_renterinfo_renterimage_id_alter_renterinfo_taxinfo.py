# Generated by Django 4.1 on 2023-05-29 15:01

import authy.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authy", "0005_renterinfo_taxinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="renterinfo",
            name="renterImage_id",
            field=models.ImageField(
                blank=True,
                default=None,
                null=True,
                upload_to=authy.models.render_id_image_dir_path,
            ),
        ),
        migrations.AlterField(
            model_name="renterinfo",
            name="taxinfo",
            field=models.ImageField(
                blank=True,
                default=None,
                null=True,
                upload_to=authy.models.render_id_image_dir_path,
            ),
        ),
    ]