import os
import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

import unittest
from unittest.mock import patch, MagicMock

from core.data_access.repositories.golfhole_repository import GolfholeRepository
from core.features.golfhole.queries.get.get_golfholes_query import GetGolfholesQuery
from core.features.golfhole.queries.get.get_golfholes_query_handler import GetGolfholesQueryHandler


class TestGetGolfholesQueryHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=GolfholeRepository)
        self.handler = GetGolfholesQueryHandler()
        self.handler.golfhole_repository = self.mock_repository
        self.golfcourseid = 1  # Mock golfcourseid

    @patch('core.features.golfhole.queries.get.get_golfholes_query_serializer.GetGolfholesQuerySerializer.is_valid',
           return_value=True)
    @patch('core.features.golfhole.queries.get.get_golfholes_query_serializer.GetGolfholesQuerySerializer.errors',
           new_callable=MagicMock)
    def test_handle_success_with_golfholes(self, mock_validated_data, mock_is_valid):
        # Arrange
        mock_golfholes = [MagicMock(), MagicMock()]
        self.mock_repository.get_list_by_key.return_value = mock_golfholes
        query = GetGolfholesQuery(golfcourseid=self.golfcourseid, page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), len(mock_golfholes))
        self.mock_repository.get_list_by_key.assert_called_once_with(golfcourseid=self.golfcourseid)

    @patch('core.features.golfhole.queries.get.get_golfholes_query_serializer.GetGolfholesQuerySerializer.is_valid',
           return_value=True)
    def test_handle_no_golfholes(self, mock_is_valid):
        # Arrange
        self.mock_repository.get_list_by_key.return_value = []
        query = GetGolfholesQuery(golfcourseid=self.golfcourseid, page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 204)
        self.assertEqual(result.value, [])
        self.mock_repository.get_list_by_key.assert_called_once_with(golfcourseid=self.golfcourseid)

    @patch('core.features.golfhole.queries.get.get_golfholes_query_serializer.GetGolfholesQuerySerializer.is_valid',
           return_value=True)
    def test_handle_pagination(self, mock_is_valid):
        # Arrange
        mock_golfholes = [MagicMock() for _ in range(10)]  # Create 10 mock golfholes
        self.mock_repository.get_list_by_key.return_value = mock_golfholes
        query = GetGolfholesQuery(golfcourseid=self.golfcourseid, page=1, page_size=5)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), 5)  # Only 5 golfholes should be returned due to pagination
        self.mock_repository.get_list_by_key.assert_called_once_with(golfcourseid=self.golfcourseid)

if __name__ == '__main__':
    unittest.main()
