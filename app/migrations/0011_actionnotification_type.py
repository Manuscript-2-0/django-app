# Generated by Django 4.1.5 on 2023-02-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_actionnotification"),
    ]

    operations = [
        migrations.AddField(
            model_name="actionnotification",
            name="type",
            field=models.CharField(
                choices=[("join", "join"), ("invite", "invite"), ("kick", "kick")],
                default="join",
                max_length=20,
            ),
        ),
    ]
