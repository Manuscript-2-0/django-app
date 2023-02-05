from django.urls import path
import app.views as views
urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('events/<int:event_id>', views.event_details, name='event_details'),
    path('events/<int:event_id>/teams',
         views.event_teams, name='event_teams'),
    path('events/<int:event_id>/teams/<int:team_id>/about',
         views.event_teams_about, name='event_teams_about'),
    #     path('events/<int:event_id>/teams/<int:team_id>/join',
    #          views.event_teams_join, name='event_teams_join'),
    #     path('events/<int:event_id>/teams/<int:team_id>/members/<int:user_id>/kick',
    #          views.event_teams_join, name='event_teams_join'),
    path('events/<int:event_id>/teams/create',
         views.create_event_team, name='create_event_team'),
    path('events/tags/<str:tag>', views.events_by_tag, name='events_by_tag'),
]
