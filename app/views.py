from rest_framework import mixins
from rest_framework.generics import GenericAPIView
import app.serializers as serializers
from app.models import Event
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


class CreateListEvents(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    """ View class for Create a new event and list all the events """
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()

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


class RetrieveUpdateDeleteEvent(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                GenericAPIView):
    """ View class for Retrieve, Update and Delete a event """
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()

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
