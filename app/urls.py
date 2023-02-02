from django.urls import path
import app.views as views
urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('events/<int:event_id>', views.event_details, name='event_details'),
    path('events/<int:event_id>/teams',
         views.event_teams, name='event_teams'),
    path('events/<int:event_id>/teams/create',
         views.create_event_team, name='create_event_team'),
    path('events/tags/<str:tag>', views.events_by_tag, name='events_by_tag'),
]
