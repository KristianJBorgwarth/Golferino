from unittest.mock import MagicMock, patch

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
        mediator.send.return_value = MagicMock(is_success=True, value={'locationname': 'TestLocation', 'address': '123 Test Address', 'city': 'TestCity'}, status_code=201)

        data = {
            'locationname': 'TestLocation',
            'address': '123 Test Address',
            'city': 'TestCity'
        }

        # Act
        response = self.client.post('/locations/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ResponseEnvelope.success(mediator.send.return_value.value, 201).to_response().data)

    @patch('core.views.location_view.get_mediator')
    def test_create_location_failure(self, mock_get_mediator):
        # Arrange
        mediator = MagicMock()
        mock_get_mediator.return_value = mediator
        mediator.send.return_value = MagicMock(is_success=False, error='Error creating location', status_code=400)

        data = {
            'locationname': 'TestLocation',
            'address': '123 Test Address',
            'city': 'TestCity'
        }

        # Act
        response = self.client.post('/locations/', data, format='json')

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ResponseEnvelope.fail('Error creating location', 400).to_response().data)

