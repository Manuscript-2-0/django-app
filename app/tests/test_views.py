from django.test import TestCase
from django.contrib.auth.models import User
from app.models import User, Event, EventType
from rest_framework.test import APIClient
import json
from unittest.mock import patch
import datetime


def assert_auth_return_requred_data(test, content):
    test.assertEqual(content['id'], User.objects.first().id)
    test.assertEqual(content['email'], User.objects.first().email)
    test.assertEqual(content['username'], User.objects.first().username)
    test.assertIn('token', content)


class CreateListEvents(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(
            username='test_user', )
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        EventType.objects.create(name='test_event_type')
        for i in range(5):
            Event.objects.create(
                name=f'test_event_{i}',
                type=EventType.objects.first(),
                start_date='2020-01-01',
                end_date='2020-01-01',
                author=user
            )

    # @patch('app.views.CreateListEvents.get')
    def test_list_events_should_return_list_of_events_on_unauthenticated_request(self):
        # Act
        response = APIClient().get('/events/')
        # Assert
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content), 5)

    def test_list_events_should_return_list_of_events_on_authenticated_request(self):
        # Act
        response = self.client.get('/events/')
        # Assert
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(len(content), 5)

    def test_create_event_should_return_404_when_user_is_not_authenticated(self):
        # Act
        response = APIClient().post('/events/', {
            'name': 'test_event',
            'type': EventType.objects.first().id,
            'start_date': '2020-01-01',
            'end_date': '2020-01-01',
        }, format='json')
        # Assert
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.')

    def test_create_event_should_create_event_on_authenticated_request(self):
        # Act
        response = self.client.post('/events/', {
            'name': 'test_event',
            'type': EventType.objects.first().id,
            'start_date': '2020-01-01',
            'end_date': '2020-01-01',
        }, format='json')
        # Assert
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'test_event')
        self.assertEqual(content['type'], EventType.objects.first().id)
        self.assertEqual(content['start_date'], '2020-01-01')
        self.assertEqual(content['end_date'], '2020-01-01')
        self.assertEqual(Event.objects.count(), 6)


class RetrieveUpdateDeleteEventTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(
            username='test_user', )

        self.client = APIClient()
        self.client.force_authenticate(user=user)
        EventType.objects.create(name='test_event_type')
        for i in range(5):
            Event.objects.create(
                name=f'test_event_{i}',
                type=EventType.objects.first(),
                start_date='2020-01-01',
                end_date='2020-01-01',
                author=user
            )

    def test_get_event_should_return_event_when_user_is_not_authenticated(self):
        response = APIClient().get(f'/events/{Event.objects.first().id}/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'test_event_0')
        self.assertEqual(content['type'], EventType.objects.first().id)
        self.assertEqual(content['start_date'], '2020-01-01')
        self.assertEqual(content['end_date'], '2020-01-01')

    def test_get_event_should_return_event_when_user_is_authenticated(self):
        response = APIClient().get(f'/events/{Event.objects.first().id}/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'test_event_0')
        self.assertEqual(content['type'], EventType.objects.first().id)
        self.assertEqual(content['start_date'], '2020-01-01')
        self.assertEqual(content['end_date'], '2020-01-01')

    def test_patch_event_should_return_401_when_user_is_not_authenticated(self):
        response = APIClient().patch(f'/events/{Event.objects.first().id}/', {
            "name": "test_event updated",
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(Event.objects.first().name, 'test_event_0')

    def test_patch_event_should_update_event_when_user_is_authenticated(self):
        response = self.client.patch(f'/events/{Event.objects.first().id}/', {
            "name": "test_event updated",
        }, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['name'], 'test_event updated')
        self.assertEqual(Event.objects.first().name, 'test_event updated')
        self.assertEqual(Event.objects.count(), 5)

    def test_put_event_should_return_401_when_user_is_not_authenticated(self):
        response = APIClient().put(f'/events/{Event.objects.first().id}/', {
            "name": "test_event updated",
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(Event.objects.first().name, 'test_event_0')

    def test_put_event_should_update_event_when_user_is_authenticated(self):
        response = self.client.put(f'/events/{Event.objects.first().id}/', {
            "name": "test_event updated",
            "type": EventType.objects.first().id,
            "start_date": "2020-06-01",
            "end_date": "2020-06-01"
        }, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['name'], 'test_event updated')
        self.assertEqual(Event.objects.first().name, 'test_event updated')
        self.assertEqual(Event.objects.first().start_date,
                         datetime.date(2020, 6, 1))
        self.assertEqual(Event.objects.first().end_date,
                         datetime.date(2020, 6, 1))
        self.assertEqual(Event.objects.count(), 5)

    def test_delete_event_should_return_401_when_user_is_not_authenticated(self):
        response = APIClient().delete(f'/events/{Event.objects.first().id}/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(Event.objects.first().name, 'test_event_0')

    def test_delete_event_should_delete_event_when_user_is_authenticated(self):
        response = self.client.delete(f'/events/{Event.objects.first().id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Event.objects.count(), 4)


class RegisterUserView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_register_user_view_should_create_new_user(self):
        response = self.client.post('/register/', {
            "email": "test@gmail.com",
            "password": "test_password",
            "username": "test_user"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_view_should_return_required_data(self):
        response = self.client.post('/register/', {
            "email": "test@gmail.com",
            "password": "test_password",
            "username": "test_user"
        })
        content = json.loads(response.content)
        assert_auth_return_requred_data(self, content)

    def test_register_user_view_should_return_400_when_email_is_invalid(self):
        response = self.client.post('/register/', {
            "password": "test_password",
            "username": "test_user"
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(content['email'][0], 'This field is required.')

    def test_register_user_view_should_return_400_when_username_is_invalid(self):
        response = self.client.post('/register/', {
            "email": "test@gmail.com",
            "password": "test_password",
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(content['username'][0], 'This field is required.')

    def test_register_user_view_should_return_400_when_password_is_invalid(self):
        response = self.client.post('/register/', {
            "email": "test@gmail.com",
            "username": "test_user"
        })
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(content['password'][0], 'This field is required.')


class LoginUserView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        User.objects.create_user(
            username='test_user',
            email="test@gmail.com",
            password="test_password",
        )

    def test_login_user_view_should_return_required_data(self):
        response = self.client.post('/login/', {
            "email": "test@gmail.com",
            "password": "test_password",
        })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        assert_auth_return_requred_data(self, content)
