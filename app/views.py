from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
import api.models as models
from datetime import datetime
from django.utils import timezone

# Create your views here.


def index(request):
    open_events = models.Event.objects.filter(
        start_date__lte=datetime.now(), end_date__gte=datetime.now())
    context = {
        "events": open_events
    }

    return render(request, 'index.html', context=context)


def signin(request):
    if request.method == "POST":

        email = request.POST.get("email", "").lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Проверка, что пользователь существует, но студент или преподаватель не созданы
            # Это означает, что пользователь еще не прошел верификацию по почте
            # if not (
            #         Student.objects.filter(user=user).exists()
            #         or Teacher.objects.filter(user=user).exists()
            #         or Assistant.objects.filter(user=user).exists()
            # ):
            #     return HttpResponse(content=json.dumps({"user_id": user.id}), status=401)
            login(request, user)
            return redirect("/")
        return HttpResponse(status=402)
    return render(request, 'auth/signin.html')


def signup(request):
    if request.method == 'POST':
        pass
    return render(request, 'auth/signup.html')


def event_details(request, event_id):
    event = models.Event.objects.get(id=event_id)
    event.agenda = models.AgendaItem.objects.filter(
        event=event).order_by('start_date')
    for item in event.agenda:
        item.passed = item.start_date < timezone.now()
    context = {
        "event": event
    }
    return render(request, 'event/index.html', context=context)


def event_teams(request, event_id):
    event = models.Event.objects.get(id=event_id)
    teams = models.Team.objects.filter(event=event)
    context = {
        "event": event,
        "teams": teams
    }
    return render(request, 'event/teams.html', context=context)


def events_by_tag(request, tag):
    events = models.Event.objects.filter(tags__name__in=[tag])
    context = {
        "events": events
    }

    return render(request, 'index.html', context=context)
