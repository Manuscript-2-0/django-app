from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from app.serializers import EventSerializer
from app.models import Event, User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class CreateListEvents(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    """ View class for Create a new event and list all the events """
    serializer_class = EventSerializer
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
    serializer_class = EventSerializer
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
