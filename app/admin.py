from django.contrib import admin
from app.models import ManuscriptUser, EventType, Event
# Register your models here.
admin.site.register(ManuscriptUser)
admin.site.register(EventType)
admin.site.register(Event)
