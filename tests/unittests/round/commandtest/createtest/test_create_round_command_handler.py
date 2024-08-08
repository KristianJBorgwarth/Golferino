import os
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.commands.round.create.create_round_command import CreateRoundCommand
from core.commands.round.create.create_round_command_handler import CreateRoundCommandHandler
from core.data_access.models.round_model import Round
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.data_access.repositories.round_repository import RoundRepository

class TestCreateRoundCommandHandler(unittest.TestCase):

    def setUp(self):
        self.handler = CreateRoundCommandHandler()
        self.handler.round_repository = MagicMock(spec=RoundRepository)
        self.handler.golfcourse_repository = MagicMock(spec=GolfcourseRepository)

    @patch('core.commands.round.create.create_round_command_handler.Round', autospec=True)
    def test_handle_given_valid_command_should_create_and_return_result_ok(self, MockRound):
        # Arrange
        command = CreateRoundCommand(
            golfcourseid=1,
            dateplayed='20230722'
        )

        mock_round_instance = MockRound.return_value
        mock_round_instance.roundid = 420
        mock_round_instance.golfcourseid = 1
        mock_round_instance.dateplayed = '20230722'

        self.handler.golfcourse_repository.golfcourse_exists.return_value = True
        self.handler.round_repository.create.return_value = mock_round_instance

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.value, {'roundid': 420, 'dateplayed': '20230722', 'golfcourseid': 1})
        self.handler.golfcourse_repository.golfcourse_exists.assert_called_once_with(golfcourseid=1)
        self.handler.round_repository.create.assert_called_once_with(mock_round_instance)

    @patch('core.commands.round.create.create_round_command_handler.datetime', wraps=datetime)
    @patch('core.commands.round.create.create_round_command_handler.Round', autospec=True)
    def test_handle_should_set_dateplayed_if_not_provided(self, MockRound, mock_datetime):
        # Arrange
        mock_datetime.now.return_value = datetime(2023, 7, 22)
        command = CreateRoundCommand(
            golfcourseid=1,
            dateplayed=''
        )

        mock_round_instance = MockRound.return_value
        mock_round_instance.roundid = 69
        mock_round_instance.golfcourseid = 1
        mock_round_instance.dateplayed = '20230722'

        self.handler.golfcourse_repository.golfcourse_exists.return_value = True
        self.handler.round_repository.create.return_value = mock_round_instance

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.value, {'roundid': 69, 'dateplayed': '20230722', 'golfcourseid': 1})
        self.handler.golfcourse_repository.golfcourse_exists.assert_called_once_with(golfcourseid=1)
        self.handler.round_repository.create.assert_called_once_with(mock_round_instance)

    def test_handle_given_nonexistent_golfcourse_should_return_not_found_error(self):
        # Arrange
        command = CreateRoundCommand(
            golfcourseid=99,
            dateplayed='20230722'
        )

        self.handler.golfcourse_repository.golfcourse_exists.return_value = False

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, 'Golfcourse with id 99 not found ...')
        self.handler.golfcourse_repository.golfcourse_exists.assert_called_once_with(golfcourseid=99)
        self.handler.round_repository.create.assert_not_called()
