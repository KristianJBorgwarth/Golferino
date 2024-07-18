import os
from unittest.mock import MagicMock, patch
import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from rest_framework.test import APITestCase, APIClient

from core.views.ResponseEnvelope import ResponseEnvelope
from core.views.player_view import PlayerView


class TestPlayerView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view = PlayerView.as_view({'post': 'create'})

    @patch('core.views.player_view.get_mediator')
    def test_create_player_success(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mediator.send.return_value = MagicMock(is_success=True,
                                               value={'firstname': 'TestFirstName',
                                                      'lastname': 'TestLastName',
                                                      'email': 'test@mail.com'},
                                               status_code=201)

        data = {'firstname': 'TestFirstName',
                'lastname': 'TestLastName',
                'email': 'test@mail.com'}

        # Act
        response = self.client.post('/players/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         ResponseEnvelope.success(mediator.send.return_value.value, 201).to_response().data)

    @patch('core.views.player_view.get_mediator')
    def test_create_player_failure(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mediator.send.return_value = MagicMock(is_success=False,
                                               error='Error creating location',
                                               status_code=400)

        data = {
            'firstname': 'TestFirstName',
            'lastname': 'TestLastName',
            'email': 'test@mail.com'
        }

        # Act
        response = self.client.post('/players/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ResponseEnvelope.fail('Error creating location', 400).to_response().data)
