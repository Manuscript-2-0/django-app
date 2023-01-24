from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.


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
