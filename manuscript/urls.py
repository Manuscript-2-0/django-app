from app.views import CreateListEvents, RetrieveUpdateDeleteEvent
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', CreateListEvents.as_view(), name='create_list_events'),
    path('events/<int:pk>/', RetrieveUpdateDeleteEvent.as_view(),
         name='retrieve_update_delete_event')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
