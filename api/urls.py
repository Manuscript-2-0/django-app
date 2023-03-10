import api.views as views
import api.views_ticket as views_ticket
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='token_obtain_pair'),
    path('register', views.RegisterUserView.as_view(), name='register_user'),
    #     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events', views.CreateListEvents.as_view(), name='create_list_events'),
    path('events/<int:id>/create_team',
         views.CreateTeamForEventView.as_view(), name='create_list_events'),
    path('events/<int:pk>',
         views.RetrieveEvent.as_view(), name='retrieve_event'),
    path('tickets/', views_ticket.CreateListTicketView.as_view(),
         name='create_list_tickets'),
    path('events/<int:pk>', views.RetrieveEvent.as_view(),
         name='retrieve_update_delete_event'),
    path('tickets/<int:pk>', views_ticket.RetrieveUpdateDeleteTicketView.as_view(),
         name='retrieve_update_delete_ticket')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
