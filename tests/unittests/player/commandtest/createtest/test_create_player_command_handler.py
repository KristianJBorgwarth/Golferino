import os
import unittest
from unittest.mock import patch, MagicMock

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.commands.player.create.create_player_command_handler import CreatePlayerCommandHandler
from core.data_access.models.player_model import Player
from core.data_access.repositories.player_repository import PlayerRepository


class TestCreatePlayerCommandHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=PlayerRepository)
        self.handler = CreatePlayerCommandHandler()
        self.handler.player_repository = self.mock_repository

    @patch('core.serializers.player.create_player_cmd_serializer.CreatePlayerCommandSerializer.is_valid',
           return_value=True)
    @patch('core.serializers.player.create_player_cmd_serializer.CreatePlayerCommandSerializer.validated_data',
           new_callable=MagicMock)
    def test_handle_given_valid_command_should_create_and_return_result_ok_PlayerDto(self, mock_validated_data,
                                                                                     mock_is_valid):
        # Arrange
        mock_validated_data.__getitem__.side_effect = lambda k: {
            'firstname': 'TestFirstName',
            'address': 'TestLastName',
            'email': 'Test@mail.com'
        }[k]

        command = CreatePlayerCommand(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com'
        )

        player = Player(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com'
        )

        self.mock_repository.player_exists.return_value = False
        self.mock_repository.create.return_value = player

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertIsInstance(result.value, dict)
        self.assertEqual(result.value['firstname'], 'TestFirstName')
        self.assertEqual(result.value['lastname'], 'TestLastName')
        self.assertEqual(result.value['email'], 'Test@mail.com')
        self.mock_repository.player_exists.assert_called_once_with(email='Test@mail.com')
        self.mock_repository.create.assert_called_once_with(mock_validated_data)

    @patch('core.serializers.player.create_player_cmd_serializer.CreatePlayerCommandSerializer.is_valid',
           return_value=False)
    @patch('core.serializers.player.create_player_cmd_serializer.CreatePlayerCommandSerializer.errors',
           new_callable=MagicMock)
    def test_handle_given_invalid_command_should_return_validation_error(self, mock_errors, mock_is_valid):
        # Arrange
        mock_errors.return_value = {'error': 'Invalid data'}

        command = CreatePlayerCommand(
            firstname='TestFirstName',
            lastname='TestLastName',
            email='Test@mail.com'
        )

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, mock_errors)
        self.mock_repository.player_exists.assert_not_called()
        self.mock_repository.create.assert_not_called()

    @patch('core.serializers.player.create_player_cmd_serializer.CreatePlayerCommandSerializer.is_valid',
           return_value=True)
    @patch('core.serializers.player.create_player_cmd_serializer.CreatePlayerCommandSerializer.validated_data',
           new_callable=MagicMock)
    def test_handle_given_existing_Player_should_return_already_exists_error(self, mock_validated_data,
                                                                             mock_is_valid):
        # Arrange
        mock_validated_data.__getitem__.side_effect = lambda k: {
            'firstname': 'TestFirstName',
            'address': 'TestLastName',
            'email': 'Test@mail.com'
        }[k]

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
        self.mock_repository.create.assert_not_called()
