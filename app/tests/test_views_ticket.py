from django.test import TestCase
from django.contrib.auth.models import User
from app.models import User, Event, EventType, Ticket
from rest_framework.test import APIClient
import json
from unittest.mock import patch
import datetime


def assert_auth_return_requred_data(test, content):
    test.assertEqual(content['id'], User.objects.first().id)
    test.assertEqual(content['email'], User.objects.first().email)
    test.assertEqual(content['username'], User.objects.first().username)
    test.assertIn('token', content)


class CreateListTickets(TestCase):
    def create_list_of_tickets(self):
        for i in range(5):
            Ticket.objects.create(
                event=self.event,
                user=self.user
            )

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test_user', )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        EventType.objects.create(name='test_ticket_type')

        self.event = Event.objects.create(
            name=f'test_ticket',
            type=EventType.objects.first(),
            start_date='2020-01-01',
            end_date='2020-01-01',
            author=self.user
        )

    # @patch('app.views.CreateListEvents.get')
    def test_list_tickets_should_return_list_of_tickets_on_unauthenticated_request(self):
        self.create_list_of_tickets()
        response = APIClient().get('/tickets/')
        content = json.loads(response.content)
        self.assertEqual(len(content), 5)
        self.assertEqual(response.status_code, 200)

    def test_list_tickets_should_return_list_of_tickets_on_authenticated_request(self):
        self.create_list_of_tickets()
        response = self.client.get('/tickets/')
        content = json.loads(response.content)
        self.assertEqual(len(content), 5)
        self.assertEqual(response.status_code, 200)

    def test_create_ticket_should_return_404_when_user_is_not_authenticated(self):
        response = APIClient().post('/tickets/', {
            'event': self.event.id,
        }, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.')

    def test_create_ticket_should_create_ticket_on_authenticated_request(self):
        response = self.client.post('/tickets/', {
            'event': self.event.id,
        }, format='json')
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['user'], self.user.id)
        self.assertEqual(content['event_details']['id'], self.event.id)
        self.assertEqual(content['status'], 'pending')
        self.assertEqual(Ticket.objects.count(), 1)


class RetrieveUpdateDeleteEventTest(TestCase):
    def create_list_of_tickets(self):
        for i in range(5):
            Ticket.objects.create(
                event=self.event,
                user=self.user
            )

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test_user', )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        EventType.objects.create(name='test_ticket_type')

        self.event = Event.objects.create(
            name=f'test_ticket',
            type=EventType.objects.first(),
            start_date='2020-01-01',
            end_date='2020-01-01',
            author=self.user
        )
        self.ticket = Ticket.objects.create(
            event=self.event,
            user=self.user)

    def test_get_ticket_should_return_ticket_when_user_is_not_authenticated(self):
        response = APIClient().get(f'/tickets/{self.ticket.id}/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['event_details']['id'], self.event.id)
        self.assertEqual(content['user'], self.user.id)
        self.assertEqual(content['status'], 'pending')

    def test_get_ticket_should_return_ticket_when_user_is_authenticated(self):
        response = self.client.get(f'/tickets/{self.ticket.id}/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['event_details']['id'], self.event.id)
        self.assertEqual(content['user'], self.user.id)
        self.assertEqual(content['status'], 'pending')

    def test_patch_ticket_should_return_401_when_user_is_not_authenticated(self):
        response = APIClient().patch(f'/tickets/{self.ticket.id}/', {
            "status": "activated",
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(Ticket.objects.first().status, 'pending')

    def test_patch_ticket_should_update_ticket_when_user_is_authenticated(self):
        response = self.client.patch(f'/tickets/{self.ticket.id}/', {
            "status": "activated",
        }, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.first().status, 'activated')

    def test_delete_ticket_should_return_401_when_user_is_not_authenticated(self):
        response = APIClient().delete(f'/tickets/{self.ticket.id}/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(Ticket.objects.count(), 1)

    def test_delete_ticket_should_delete_ticket_when_user_is_authenticated(self):
        response = self.client.delete(f'/tickets/{self.ticket.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ticket.objects.count(), 0)
