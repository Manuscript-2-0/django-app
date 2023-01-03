from django.contrib import admin
from app.models import User, EventType, Event
# Register your models here.
admin.site.register(User)
admin.site.register(EventType)
admin.site.register(Event)
