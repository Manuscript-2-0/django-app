from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import app.models as models
from datetime import datetime
from django.utils import timezone
import app.utils as utils
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


def event_teams_about(request, event_id, team_id):
    event = models.Event.objects.get(id=event_id)
    team = models.Team.objects.get(id=team_id)
    team_materials = models.TeamMaterial.objects.filter(team=team)
    context = {
        "event": event,
        "team": team,
        "files": [material for material in team_materials if material.file],
        "urls": [material for material in team_materials if material.url],
        "is_leader": team.leader == request.user,
        "is_member": request.user in team.members.all()
    }
    return render(request, 'team/index.html', context=context)


def create_event_team(request, event_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signin'))
    event = models.Event.objects.get(id=event_id)
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name', '')
        team = models.Team.objects.create(
            name=name, event=event, leader=user)
        image = 'images/02.jpg'
        if request.FILES.get('file', None):
            image_blob = request.FILES['file']
            path = utils.handle_uploaded_file(image_blob, str(image_blob))
            image = path
        team.image = image
        team.save()

        team.members.add(user)
        for i in range(5):
            skill_name = request.POST.get(f'option-{i}', '')
            if skill_name:
                if models.RequiredSkill.objects.filter(name=skill_name).exists():
                    skill = models.RequiredSkill.objects.get(name=skill_name)
                skill = models.RequiredSkill.objects.create(name=skill_name)
                team.required_skills.add(skill)
        team.save()
        return redirect(f'/events/{event_id}/teams')
    skills = models.RequiredSkill.objects.all()
    context = {
        "event": event,
        "skills": skills
    }
    return render(request, 'team/team_form.html', context=context)


def events_by_tag(request, tag):
    events = models.Event.objects.filter(tags__name__in=[tag])
    context = {
        "events": events
    }

    return render(request, 'index.html', context=context)
