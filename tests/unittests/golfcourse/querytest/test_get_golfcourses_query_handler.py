import os

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.queries.golfcourse.get.get_golfcourses_query import GetGolfcoursesQuery

import unittest
from unittest.mock import patch, MagicMock

from core.queries.player.get.get_players_query_handler import GetPlayersQueryHandler


class TestGetGolfcoursesQueryHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=GolfcourseRepository)
        self.handler = GetPlayersQueryHandler()
        self.handler.player_repository = self.mock_repository

    @patch('core.serializers.golfcourse.get_golfcourses_query_serializer.GetGolfcoursesQuerySerializer.is_valid',
           return_value=True)
    @patch('core.serializers.golfcourse.get_golfcourses_query_serializer.GetGolfcoursesQuerySerializer.errors',
           new_callable=MagicMock)
    def test_handle_success_with_players(self, mock_validated_data, mock_is_valid):
        # Arrange
        mock_golfcourses = [MagicMock(), MagicMock()]
        self.mock_repository.get_all.return_value = mock_golfcourses
        query = GetGolfcoursesQuery(page=1, page_size=2)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), len(mock_golfcourses))

    @patch('core.serializers.golfcourse.get_golfcourses_query_serializer.GetGolfcoursesQuerySerializer.is_valid',
           return_value=True)
    def test_handle_golfcourses(self, mock_is_valid):
        # Arrange
        self.mock_repository.get_all.return_value = []
        query = GetGolfcoursesQuery(page=1, page_size=2)

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
        mock_golfcourses = [MagicMock() for _ in range(10)]  # Create 10 mock players
        self.mock_repository.get_all.return_value = mock_golfcourses
        query = GetGolfcoursesQuery(page=1, page_size=5)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.value), 5)  # Only 5 players should be returned due to pagination
