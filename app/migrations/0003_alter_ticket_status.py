# Generated by Django 4.1.5 on 2023-01-04 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_ticket"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="status",
            field=models.CharField(
                choices=[
                    ("activated", "activated"),
                    ("pending", "pending"),
                    ("canceled", "canceled"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]