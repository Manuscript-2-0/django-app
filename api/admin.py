from django.contrib import admin
from api.models import User, EventType, Event, Ticket
# Register your models here.
admin.site.register(User)
admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Ticket)
