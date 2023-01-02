from django.db import models
from django.contrib.auth.models import User


class ManuscriptUser(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class EventType(models.Model):
    name = models.CharField(max_length=20)


class Event(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey('EventType', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(ManuscriptUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} ({self.type}): {self.start_date} - {self.end_date}'
