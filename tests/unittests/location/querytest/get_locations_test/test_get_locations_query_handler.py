import os

import django


# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

import unittest
from unittest.mock import patch, MagicMock
from core.queries.location.get.get_locations_query import GetLocationsQuery
from core.dtos.location_dto import LocationDto
from core.common.results import Result
from core.data_access.repositories.location_repository import LocationRepository
from core.queries.location.get.get_locations_query_handler import GetLocationsQueryHandler


class TestGetLocationsQueryHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=LocationRepository)
        self.handler = GetLocationsQueryHandler()
        self.handler.location_repository = self.mock_repository

    @patch('core.serializers.location.get_locations_query_serializer.GetLocationsQuerySerializer.is_valid', return_value=True)
    @patch('core.serializers.location.get_locations_query_serializer.GetLocationsQuerySerializer.validated_data', new_callable=MagicMock)
    def test_handle_success_with_locations(self, mock_validated_data, mock_is_valid):
        # Arrange
        mock_locations = [MagicMock(), MagicMock()] 
        self.mock_repository.get_all.return_value = mock_locations
        query = GetLocationsQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), len(mock_locations)) 

    @patch('core.serializers.location.get_locations_query_serializer.GetLocationsQuerySerializer.is_valid', return_value=False)
    @patch('core.serializers.location.get_locations_query_serializer.GetLocationsQuerySerializer.errors', new_callable=MagicMock)
    def test_handle_invalid_query_parameters(self, mock_errors, mock_is_valid):
        # Arrange
        mock_errors.return_value = {'error': 'Invalid data'}
        invalid_query = GetLocationsQuery(page=-1, page_size=20)

        # Act
        result = self.handler.handle(invalid_query)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.error, mock_errors)
        self.mock_repository.get_all.assert_not_called()

    @patch('core.serializers.location.get_locations_query_serializer.GetLocationsQuerySerializer.is_valid', return_value=True)
    def test_handle_no_locations(self, mock_is_valid):
        # Arrange
        self.mock_repository.get_all.return_value = []
        query = GetLocationsQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 204)
        self.assertEqual(result.value, [])

    @patch('core.serializers.location.get_locations_query_serializer.GetLocationsQuerySerializer.is_valid', return_value=True)
    def test_handle_pagination(self, mock_is_valid):
        # Arrange
        mock_locations = [MagicMock() for _ in range(10)]  # Create 10 mock locations
        self.mock_repository.get_all.return_value = mock_locations
        query = GetLocationsQuery(page=1, page_size=5)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), 5)  # Only 5 locations should be returned due to pagination

