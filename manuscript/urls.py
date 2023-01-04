import app.views as views
import app.views_ticket as views_ticket
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginUserView.as_view(), name='token_obtain_pair'),
    path('register/', views.RegisterUserView.as_view(), name='register_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', views.CreateListEvents.as_view(), name='create_list_events'),
    path('tickets/', views_ticket.CreateListTicketView.as_view(),
         name='create_list_tickets'),
    path('events/<int:pk>/', views.RetrieveUpdateDeleteEvent.as_view(),
         name='retrieve_update_delete_event'),
    path('tickets/<int:pk>/', views_ticket.RetrieveUpdateDeleteTicketView.as_view(),
         name='retrieve_update_delete_ticket')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
