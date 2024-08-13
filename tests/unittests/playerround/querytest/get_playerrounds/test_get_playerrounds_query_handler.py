import os

import django


# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

import unittest
from unittest.mock import patch, MagicMock
from core.queries.playerround.get.get_playerrounds_query import GetPlayerroundsQuery

from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.queries.playerround.get.get_playerrounds_query_handler import GetPlayerroundsQueryHandler


class TestGetPlayerroundsQueryHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=PlayerroundRepository)
        self.handler = GetPlayerroundsQueryHandler()
        self.handler.playerround_repository = self.mock_repository

    @patch('core.serializers.playerround.get_playerrounds_query_serializer.GetPlayerroundsQuerySerializer.is_valid',
           return_value=True)
    @patch('core.serializers.playerround.get_playerrounds_query_serializer.GetPlayerroundsQuerySerializer.errors',
           new_callable=MagicMock)
    def test_handle_success_with_playerrounds(self, mock_validated_data, mock_is_valid):
        # Arrange
        mock_playerrounds = [MagicMock(), MagicMock()]
        self.mock_repository.get_all.return_value = mock_playerrounds
        query = GetPlayerroundsQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), len(mock_playerrounds))

    @patch('core.serializers.playerround.get_playerrounds_query_serializer.GetPlayerroundsQuerySerializer.is_valid',
           return_value=True)
    def test_handle_no_playerrounds(self, mock_is_valid):
        # Arrange
        self.mock_repository.get_all.return_value = []
        query = GetPlayerroundsQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 204)
        self.assertEqual(result.value, [])

    @patch('core.serializers.playerround.get_playerrounds_query_serializer.GetPlayerroundsQuerySerializer.is_valid',
           return_value=True)
    def test_handle_pagination(self, mock_is_valid):
        # Arrange
        mock_playerrounds = [MagicMock() for _ in range(10)]  # Create 10 mock playerrounds
        self.mock_repository.get_all.return_value = mock_playerrounds
        query = GetPlayerroundsQuery(page=1, page_size=5)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), 5)  # Only 5 playerrounds should be returned due to pagination
