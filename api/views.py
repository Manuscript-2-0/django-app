from rest_framework import mixins
from rest_framework.generics import GenericAPIView
import api.serializers as serializers
import api.models as models
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


class CreateListEvents(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    """ View class for Create a new event and list all the events """
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    def get_permissions(self):
        method = self.request.method
        if method == 'GET':
            return []
        else:
            return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        """ Get all events, here we are using the .list method available in the mixins.ListModelMixin """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Create a new event, here we are using the .create method available in the mixins.CreateModelMixin """
        request.data['author'] = request.user.id
        return self.create(request, *args, **kwargs)


class RetrieveEvent(mixins.RetrieveModelMixin,  GenericAPIView):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """ .retrieve method available in the mixins.RetrieveModelMixin """
        return self.retrieve(request, *args, **kwargs)


class RetrieveEvent(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericAPIView):
    """ View class for Retrieve, Update and Delete a event """
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    def get_permissions(self):
        method = self.request.method
        if method == 'GET':
            return []
        else:
            return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        """ .retrieve method available in the mixins.RetrieveModelMixin """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        """ .partial_update method available in the mixins.UpdateModelMixin """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ .destroy method available in the mixins.DestroyModelMixin """
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        """ .update method available in the mixins.UpdateModelMixin """
        return self.update(request, *args, **kwargs)


class LoginUserView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUserView(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegistrationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CreateTeamForEventView(mixins.CreateModelMixin, GenericAPIView):
    """ View class for Create a new team for an event """
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """ Create a new team for an event, here we are using the .create method available in the mixins.CreateModelMixin """
        if "name" not in request.data or request.data['name'] == '':
            return Response({'error': 'Team name is required'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['users'] = [request.user.id]
        request.data['event'] = kwargs['id']
        return self.create(request, *args, **kwargs)
