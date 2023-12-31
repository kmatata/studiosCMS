# Generated by Django 4.1 on 2023-05-29 12:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("authy", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="groups",
        ),
        migrations.AlterField(
            model_name="renterinfo",
            name="natId",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=8,
                null=True,
                unique=True,
                validators=[django.core.validators.RegexValidator("^[0-9]+$")],
                verbose_name="National ID",
            ),
        ),
        migrations.AlterField(
            model_name="renterinfo",
            name="renter",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="renterProfile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
