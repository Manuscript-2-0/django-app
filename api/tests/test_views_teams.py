from django.test import TestCase
from django.contrib.auth.models import User
from api.models import User, Event, EventType, Ticket
from rest_framework.test import APIClient
import json
from unittest.mock import patch


class CreateTeam(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test_user', )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_team_should_raise_exception_when_user_is_not_authenticated(self):
        response = APIClient().post('/events/999/create_team', {
            'name': 'test_team',
        }, format='json')

        self.assertEqual(response.status_code, 403)

    def test_create_team_should_raise_exception_when_event_does_not_exist(self):
        response = self.client.post('/events/999/create_team', {
            'name': 'test_team',
        }, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['event'][0],
                         'Invalid pk "999" - object does not exist.')

    def test_create_team_should_raise_exception_when_team_data_is_not_valid(self):
        event = Event.objects.create(
            name='test_event',
            type=EventType.objects.create(name='test_event_type'),
            start_date='2020-01-01',
            end_date='2020-01-01',
            author=self.user
        )
        response = self.client.post(f'/events/{event.id}/create_team', {
            'name': '',
        }, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['error'], 'Team name is required')

    def test_create_team_should_create_team(self):
        event = Event.objects.create(
            name='test_event',
            type=EventType.objects.create(name='test_event_type'),
            start_date='2020-01-01',
            end_date='2020-01-01',
            author=self.user
        )
        response = self.client.post(f'/events/{event.id}/create_team', {
            'name': 'test_team',
        }, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content['name'], 'test_team')
        self.assertEqual(content['event'], event.id)
        self.assertEqual(content['users'], [self.user.id])
