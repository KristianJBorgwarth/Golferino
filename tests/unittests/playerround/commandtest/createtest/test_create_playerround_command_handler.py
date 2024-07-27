import os
import unittest
import django
from unittest.mock import Mock
from datetime import datetime, timedelta

from core.data_access.models.player_model import Player
from core.data_access.repositories.player_repository import PlayerRepository

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.serializers.playerround.create_playerround_cmd_serializer import CreatePlayerroundCommandSerializer
from core.commands.playerround.create.create_playerround_command import CreatePlayerroundCommand
from core.common.results import Result
from core.dtos.playerround_dto import PlayerroundDto
from core.common.error_messages import ErrorMessage
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.round_model import Round
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.data_access.repositories.round_repository import RoundRepository
from core.commands.playerround.create.create_playerround_command_handler import CreatePlayerroundCommandHandler


class TestCreatePlayerroundCommandHandler(unittest.TestCase):

    def setUp(self):
        self.playerround_repository_mock = Mock(spec=PlayerroundRepository)
        self.round_repository_mock = Mock(spec=RoundRepository)
        self.player_repository_mock = Mock(spec=PlayerRepository)
        self.handler = CreatePlayerroundCommandHandler()
        self.handler.playerround_repository = self.playerround_repository_mock
        self.handler.round_repository = self.round_repository_mock

    def test_handle_with_valid_command(self):
        # Arrange
        self.player_repository_mock.player_exists.return_value = True
        player = Player()
        self.player_repository_mock.create.return_value = player
        self.round_repository_mock.round_exists.return_value = True

        round = Round()
        self.round_repository_mock.create.return_value = round  # Create a Round instance

        command = CreatePlayerroundCommand(playerid=69,
                                           roundid=420
                                           )

        self.playerround_repository_mock.create.return_value = Playerround(playerid=player.playerid,
                                                                           roundid=round.roundid)

        # Act
        result = self.handler.handle(command)
        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.playerround_repository_mock.create.assert_called_once()

    def test_handle_with_invalid_serializer_data(self):
        # Arrange
        command = CreatePlayerroundCommand(playerid=None, roundid=1)  # Invalid data: playerid is None

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.status_code, 400)
        self.assertIn('playerid', result.error)  # Assuming 'error' is the correct attribute

    def test_handle_with_non_existent_round(self):
        # Arrange
        command = CreatePlayerroundCommand(playerid=1, roundid=999)  # Non-existent roundid
        self.round_repository_mock.round_exists.return_value = False

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.status_code, 400)
        self.assertIn('round with id 999 not found', result.error)  # Assuming 'error' is the correct attribute

    def test_handle_with_missing_playerid(self):
        # Arrange
        invalid_command = CreatePlayerroundCommand(playerid=None, roundid=1)  # Missing playerid

        # Act
        result = self.handler.handle(invalid_command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.status_code, 400)
        self.assertIn('playerid', result.error)  # Assuming 'error' is the correct attribute

    def test_handle_with_missing_roundid(self):
        # Arrange
        invalid_command = CreatePlayerroundCommand(playerid=1, roundid=None)  # Missing roundid

        # Act
        result = self.handler.handle(invalid_command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.status_code, 400)
        self.assertIn('roundid', result.error)  # Assuming 'error' is the correct attribute


if __name__ == '__main__':
    unittest.main()
