from django.urls import path
import app.views as views
urlpatterns = [
    path('login', views.login, name='login'),
]
