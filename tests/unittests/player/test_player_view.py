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
        
        # Mock the result of the mediator send2 method
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.value = {
            'firstname': 'TestFirstName',
            'lastname': 'TestLastName',
            'email': 'test@mail.com'
        }
        mock_response.status_code = 201
        mediator.send2.return_value = mock_response

        data = {
            'firstname': 'TestFirstName',
            'lastname': 'TestLastName',
            'email': 'test@mail.com'
        }

        # Act
        response = self.client.post('/players/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 201)
        expected_response = ResponseEnvelope.success(mock_response.value, 201).data
        self.assertEqual(response.json(), expected_response)

    @patch('core.views.player_view.get_mediator')
    def test_create_player_failure(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        
        # Mock the result of the mediator send2 method
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.error = 'Error creating player'
        mock_response.status_code = 400
        mediator.send2.return_value = mock_response

        data = {
            'firstname': 'TestFirstName',
            'lastname': 'TestLastName',
            'email': 'test@mail.com'
        }

        # Act
        response = self.client.post('/players/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 400)
        expected_response = ResponseEnvelope.fail('Error creating player', 400).data
        self.assertEqual(response.json(), expected_response)
