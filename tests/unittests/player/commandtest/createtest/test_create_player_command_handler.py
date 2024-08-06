from unittest.mock import MagicMock, patch
from unittest import TestCase
from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.commands.player.create.create_player_command_handler import CreatePlayerCommandHandler
from core.data_access.repositories.player_repository import PlayerRepository
from core.data_access.models.player_model import Player
from core.common.results import Result

class TestCreatePlayerCommandHandler(TestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=PlayerRepository)
        self.handler = CreatePlayerCommandHandler()
        self.handler.player_repository = self.mock_repository

    def test_handle_given_existing_player_should_return_already_exists_error(self):
        # Arrange
        command = CreatePlayerCommand(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com'
        )

        self.mock_repository.player_exists.return_value = True

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, 'A player with this Test@mail.com already exists.')
        self.mock_repository.player_exists.assert_called_once_with(email='Test@mail.com')
        self.mock_repository.create_2.assert_not_called()

    def test_handle_given_valid_command_should_create_and_return_result_ok_playerDto(self):
        # Arrange
        command = CreatePlayerCommand(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com'
        )

        self.mock_repository.player_exists.return_value = False

        player = Player(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com'
        )

        # Mock the create_2 method to return a real Player instance
        self.mock_repository.create_2.return_value = player

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertIsInstance(result.value, dict)
        self.assertEqual(result.value['firstname'], 'TestFirstName')
        self.assertEqual(result.value['lastname'], 'TestLastName')
        self.assertEqual(result.value['email'], 'Test@mail.com')
        self.mock_repository.player_exists.assert_called_once_with(email='Test@mail.com')
        self.mock_repository.create_2.assert_called_once()