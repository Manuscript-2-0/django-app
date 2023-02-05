from django.contrib import admin
from app.models import User, EventType, Event, Ticket, EventTag, AgendaItem, Team, ActionNotification
# Register your models here.
admin.site.register(User)
admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(EventTag)
admin.site.register(AgendaItem)
admin.site.register(Team)
admin.site.register(ActionNotification)
