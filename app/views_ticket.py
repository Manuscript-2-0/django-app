from rest_framework import mixins
from rest_framework.generics import GenericAPIView
import app.serializers as serializers
from app.models import Ticket
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


class CreateListTicketView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    """ View class for Create a new ticket and list all the events """
    serializer_class = serializers.TicketSerializer
    queryset = Ticket.objects.all()

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


class RetrieveUpdateDeleteTicketView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin,
                                     GenericAPIView):
    """ View class for Retrieve, Update and Delete a event """
    serializer_class = serializers.TicketSerializer
    queryset = Ticket.objects.all()

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
        request.data['user'] = request.user.id
        """ .partial_update method available in the mixins.UpdateModelMixin """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ .destroy method available in the mixins.DestroyModelMixin """
        return self.destroy(request, *args, **kwargs)
