import os

import django

from core.data_access.repositories.round_repository import RoundRepository
from core.features.round.queries.get.get_rounds_query import GetRoundsQuery
from core.features.round.queries.get.get_rounds_query_handler import GetRoundsQueryHandler

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

import unittest
from unittest.mock import patch, MagicMock



class TestGetRoundsQueryHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=RoundRepository)
        self.handler = GetRoundsQueryHandler()
        self.handler.round_repository = self.mock_repository

    @patch('core.features.round.queries.get.get_rounds_query_serializer.GetRoundsQuerySerializer.is_valid',
           return_value=True)
    @patch('core.features.round.queries.get.get_rounds_query_serializer.GetRoundsQuerySerializer.errors',
           new_callable=MagicMock)
    def test_handle_success_with_rounds(self, mock_validated_data, mock_is_valid):
        # Arrange
        mock_rounds = [MagicMock(), MagicMock()]
        self.mock_repository.get_all.return_value = mock_rounds
        query = GetRoundsQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), len(mock_rounds))

    @patch('core.features.round.queries.get.get_rounds_query_serializer.GetRoundsQuerySerializer.is_valid',
           return_value=True)
    def test_handle_no_rounds(self, mock_is_valid):
        # Arrange
        self.mock_repository.get_all.return_value = []
        query = GetRoundsQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 204)
        self.assertEqual(result.value, [])

    @patch('core.features.round.queries.get.get_rounds_query_serializer.GetRoundsQuerySerializer.is_valid',
           return_value=True)
    def test_handle_pagination(self, mock_is_valid):
        # Arrange
        mock_rounds = [MagicMock() for _ in range(10)]  # Create 10 mock rounds
        self.mock_repository.get_all.return_value = mock_rounds
        query = GetRoundsQuery(page=1, page_size=5)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), 5)  # Only 5 rounds should be returned due to pagination
