import os
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.commands.round.create.create_round_command import CreateRoundCommand
from core.common.error_messages import ErrorMessage
from core.data_access.models.round_model import Round
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.data_access.repositories.round_repository import RoundRepository
from core.commands.round.create.create_round_command_handler import CreateRoundCommandHandler


class TestCreateRoundCommandHandler(unittest.TestCase):

    def setUp(self):
        self.handler = CreateRoundCommandHandler()
        self.handler.round_repository = MagicMock(spec=RoundRepository)
        self.handler.golfcourse_repository = MagicMock(spec=GolfcourseRepository)

    @patch('core.serializers.round.create_round_cmd_serializer.CreateRoundCommandSerializer.is_valid',
           return_value=True)
    @patch('core.serializers.round.create_round_cmd_serializer.CreateRoundCommandSerializer.validated_data',
           new_callable=MagicMock)
    def test_handle_given_valid_command_should_create_and_return_result_ok(self, mock_validated_data, mock_is_valid):
        # Arrange
        command = CreateRoundCommand(
            golfcourseid='1',
            dateplayed='20230722'
        )

        mock_validated_data.__getitem__.side_effect = lambda k: {
            'golfcourseid': '1',
            'dateplayed': '20230722'
        }[k]

        round_instance = MagicMock(spec=Round)
        round_instance.roundid = 420
        round_instance.golfcourseid = '1'
        round_instance.dateplayed = '20230722'
        self.handler.golfcourse_repository.golfcourse_exists.return_value = True
        self.handler.round_repository.create.return_value = round_instance

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.value, {'roundid': 420, 'dateplayed': '20230722', 'golfcourseid': '1'})
        self.handler.golfcourse_repository.golfcourse_exists.assert_called_once_with(golfcourseid='1')
        self.handler.round_repository.create.assert_called_once_with(mock_validated_data)

    @patch('core.serializers.round.create_round_cmd_serializer.CreateRoundCommandSerializer.errors',
           new_callable=MagicMock)
    def test_handle_given_invalid_golfcourse_should_return_wrong_type_error(self, mock_errors):
        # Arrange
        mock_errors.return_value = {'golfcourseid': 'invalid_id must be of type integer'}
        command = CreateRoundCommand(
            golfcourseid='invalid_id',
            dateplayed='2023-07-22'
        )

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, mock_errors)
        self.handler.round_repository.create.assert_not_called()

    @patch('core.serializers.round.create_round_cmd_serializer.CreateRoundCommandSerializer.is_valid',
           return_value=True)
    @patch('core.serializers.round.create_round_cmd_serializer.CreateRoundCommandSerializer.validated_data',
           new_callable=MagicMock)
    def test_handle_should_set_dateplayed_if_not_provided(self, mock_validated_data, mock_is_valid):
        # Arrange
        command = CreateRoundCommand(
            golfcourseid='1',
            dateplayed=''
        )

        mock_validated_data.__getitem__.side_effect = lambda k: {
            'golfcourseid': '1',
            'dateplayed': datetime.now().strftime(format="%Y%m%d")
        }[k]

        round_instance = MagicMock(spec=Round)
        round_instance.roundid = 69
        round_instance.golfcourseid = '1'
        round_instance.dateplayed = datetime.now().strftime(format="%Y%m%d")
        self.handler.golfcourse_repository.golfcourse_exists.return_value = True
        self.handler.round_repository.create.return_value = round_instance

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertEqual(result.value, {'roundid': 69,
                                        'golfcourseid': '1',
                                        'dateplayed': datetime.now().strftime(format="%Y%m%d")})
        self.handler.golfcourse_repository.golfcourse_exists.assert_called_once_with(golfcourseid='1')
        self.handler.round_repository.create.assert_called_once_with(mock_validated_data)


if __name__ == '__main__':
    unittest.main()
