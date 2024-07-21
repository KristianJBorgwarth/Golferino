import os

import django


# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

import unittest
from unittest.mock import patch, MagicMock
from core.queries.player.get.get_players_query import GetPlayersQuery

from core.data_access.repositories.player_repository import PlayerRepository
from core.queries.player.get.get_players_query_handler import GetPlayersQueryHandler


class TestGetPlayersQueryHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=PlayerRepository)
        self.handler = GetPlayersQueryHandler()
        self.handler.player_repository = self.mock_repository

    @patch('core.serializers.player.get_players_query_serializer.GetPlayersQuerySerializer.is_valid',
           return_value=False)
    @patch('core.serializers.player.get_players_query_serializer.GetPlayersQuerySerializer.errors',
           new_callable=MagicMock)
    def test_handle_success_with_players(self, mock_validated_data, mock_is_valid):
        # Arrange
        mock_players = [MagicMock(), MagicMock()]
        self.mock_repository.get_all.return_value = mock_players
        query = GetPlayersQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), len(mock_players))

    @patch('core.serializers.player.get_players_query_serializer.GetPlayersQuerySerializer.is_valid',
           return_value=False)
    @patch('core.serializers.player.get_players_query_serializer.GetPlayersQuerySerializer.errors',
           new_callable=MagicMock)
    def test_handle_invalid_query_parameters(self, mock_errors, mock_is_valid):
        # Arrange
        mock_errors.return_value = {'error': 'Invalid data'}
        invalid_query = GetPlayersQuery(page=-1, page_size=20)

        # Act
        result = self.handler.handle(invalid_query)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.error, mock_errors)
        self.mock_repository.get_all.assert_not_called()

    @patch('core.serializers.player.get_players_query_serializer.GetPlayersQuerySerializer.is_valid',
           return_value=True)
    def test_handle_no_players(self, mock_is_valid):
        # Arrange
        self.mock_repository.get_all.return_value = []
        query = GetPlayersQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 204)
        self.assertEqual(result.value, [])

    @patch('core.serializers.player.get_players_query_serializer.GetPlayersQuerySerializer.is_valid',
           return_value=True)
    def test_handle_pagination(self, mock_is_valid):
        # Arrange
        mock_players = [MagicMock() for _ in range(10)]  # Create 10 mock players
        self.mock_repository.get_all.return_value = mock_players
        query = GetPlayersQuery(page=1, page_size=5)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), 5)  # Only 5 players should be returned due to pagination
