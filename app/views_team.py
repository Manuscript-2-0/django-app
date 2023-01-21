from rest_framework import mixins
from rest_framework.generics import GenericAPIView
import app.serializers as serializers
import app.models as models
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


class CreateListTeamView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    """ View class for Create a new ticket and list all the events """
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()

    def get_permissions(self):
        method = self.request.method
        if method == 'GET':
            return []
        else:
            return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        """ Get all tickets, here we are using the .list method available in the mixins.ListModelMixin """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Create a new ticket, here we are using the .create method available in the mixins.CreateModelMixin """
        request.data['user'] = request.user.id
        return self.create(request, *args, **kwargs)
