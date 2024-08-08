import os
import unittest
import django
from unittest.mock import Mock

from core.data_access.models.player_model import Player

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.commands.playerround.create.create_playerround_command import CreatePlayerroundCommand
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.round_model import Round
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.data_access.repositories.round_repository import RoundRepository
from core.commands.playerround.create.create_playerround_command_handler import CreatePlayerroundCommandHandler

class TestCreatePlayerroundCommandHandler(unittest.TestCase):

    def setUp(self):
        self.playerround_repository_mock = Mock(spec=PlayerroundRepository)
        self.round_repository_mock = Mock(spec=RoundRepository)
        self.handler = CreatePlayerroundCommandHandler()
        self.handler.playerround_repository = self.playerround_repository_mock
        self.handler.round_repository = self.round_repository_mock

    def test_handle_with_valid_command(self):
        # Arrange
        self.round_repository_mock.round_exists.return_value = True

        round_instance = Round()
        player_instance = Player()
        playerround_instance = Playerround(playerid=player_instance.playerid, roundid=round_instance.roundid)

        command = CreatePlayerroundCommand(playerid=69, roundid=420)
        self.playerround_repository_mock.create.return_value = playerround_instance

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.status_code, 200)
        self.playerround_repository_mock.create.assert_called_once()

    def test_handle_with_non_existent_round(self):
        # Arrange
        command = CreatePlayerroundCommand(playerid=1, roundid=999)  # Non-existent roundid
        self.round_repository_mock.round_exists.return_value = False

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.status_code, 400)
        self.assertIn('round with id 999 not found', result.error)  
