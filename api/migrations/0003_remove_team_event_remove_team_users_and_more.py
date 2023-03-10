# Generated by Django 4.1.5 on 2023-01-25 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_event_description_event_image"),
    ]

    operations = [
        migrations.RemoveField(model_name="team", name="event",),
        migrations.RemoveField(model_name="team", name="users",),
        migrations.RemoveField(model_name="ticket", name="event",),
        migrations.RemoveField(model_name="ticket", name="user",),
        migrations.RemoveField(model_name="user", name="groups",),
        migrations.RemoveField(model_name="user", name="user_permissions",),
        migrations.DeleteModel(name="Event",),
        migrations.DeleteModel(name="EventType",),
        migrations.DeleteModel(name="Team",),
        migrations.DeleteModel(name="Ticket",),
        migrations.DeleteModel(name="User",),
    ]
