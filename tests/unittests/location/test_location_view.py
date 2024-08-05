import os
from unittest.mock import MagicMock, patch
import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.views.ResponseEnvelope import ResponseEnvelope
from core.views.location_view import LocationView


class TestLocationView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.view = LocationView.as_view({'post': 'create'})

    @patch('core.views.location_view.get_mediator')
    def test_create_location_success(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.value = {
            'locationname': 'TestLocation',
            'address': '123 Test Address',
            'city': 'TestCity'
        }
        mock_response.status_code = 201
        mediator.send2.return_value = mock_response

        data = {
            'locationname': 'TestLocation',
            'address': '123 Test Address',
            'city': 'TestCity'
        }

        # Act
        response = self.client.post('/locations/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 201)
        expected_response = ResponseEnvelope.success(mock_response.value, 201).data
        self.assertEqual(response.json(), expected_response)

    @patch('core.views.location_view.get_mediator')
    def test_create_location_failure(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.error = 'Error creating location'
        mock_response.status_code = 400
        mediator.send2.return_value = mock_response

        data = {
            'locationname': 'TestLocation',
            'address': '123 Test Address',
            'city': 'TestCity'
        }

        # Act
        response = self.client.post('/locations/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ResponseEnvelope.fail('Error creating location', 400).data)

    @patch('core.views.location_view.get_mediator')
    def test_get_all_locations_success(self, mock_get_mediator):
    # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.value = [
            {'locationname': 'Location1', 'address': 'Address1', 'city': 'City1'},
            {'locationname': 'Location2', 'address': 'Address2', 'city': 'City2'}
        ]
        mock_response.status_code = 200
        mediator.send2.return_value = mock_response

        # Act
        response = self.client.get('/locations/get_all', {'page': 1, 'page_size': 2})

        # Assert
        expected_response = {
            'success': True,
            'data': [
                {'locationname': 'Location1', 'address': 'Address1', 'city': 'City1'},
                {'locationname': 'Location2', 'address': 'Address2', 'city': 'City2'}
            ],
            'error': None
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    @patch('core.views.location_view.get_mediator')
    def test_get_all_locations_no_content(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.value = []
        mock_response.status_code = 204
        mediator.send2.return_value = mock_response

        # Act
        response = self.client.get('/locations/get_all', {'page': 1, 'page_size': 10})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    @patch('core.views.location_view.get_mediator')
    def test_get_all_locations_failure(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.error = 'Error retrieving locations'
        mock_response.status_code = 400
        mediator.send2.return_value = mock_response

        # Act
        response = self.client.get('/locations/get_all', {'page': 1, 'page_size': 10})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ResponseEnvelope.fail('Error retrieving locations', 400).data)