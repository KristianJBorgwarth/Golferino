import os
import unittest
from unittest.mock import MagicMock, patch
import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.views.ResponseEnvelope import ResponseEnvelope
from core.views.round_view import RoundView


class TestRoundView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view = RoundView.as_view({'post': 'create'})

    @patch('core.views.round_view.get_mediator')
    def test_create_round_success(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.value = {
            'golfcourseid': '1',
            'dateplayed': '2023-07-22'
        }
        mock_response.status_code = 201
        mediator.send2.return_value = mock_response

        data = {
            'golfcourseid': '1',
            'dateplayed': '2023-07-22'
        }

        # Act
        response = self.client.post('/rounds/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 201)
        expected_response = ResponseEnvelope.success(mock_response.value, 201).data
        self.assertEqual(response.json(), expected_response)

    @patch('core.views.round_view.get_mediator')
    def test_create_round_failure(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mediator.send2.return_value = MagicMock(is_success=False, error='Error creating round', status_code=400)

        data = {
            'golfcourseid': '1',
            'dateplayed': '2023-07-22'
        }

        # Act
        response = self.client.post('/rounds/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ResponseEnvelope.fail('Error creating round', 400).data)


if __name__ == '__main__':
    unittest.main()
