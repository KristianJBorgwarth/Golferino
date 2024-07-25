import os

import django
# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

import unittest
from unittest.mock import patch, MagicMock
from core.commands.location.create.create_location_command import CreateLocationCommand
from core.commands.location.create.create_location_command_handler import CreateLocationCommandHandler
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository


class TestCreateLocationCommandHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=LocationRepository)
        self.handler = CreateLocationCommandHandler()
        self.handler.location_repository = self.mock_repository

    @patch('core.serializers.location.create_location_cmd_serializer.CreateLocationCommandSerializer.is_valid', return_value=True)
    @patch('core.serializers.location.create_location_cmd_serializer.CreateLocationCommandSerializer.validated_data', new_callable=MagicMock)
    def test_handle_given_valid_command_should_create_and_return_result_ok_LocationDto(self, mock_validated_data, mock_is_valid):
        # Arrange
        mock_validated_data.__getitem__.side_effect = lambda k: {
            'locationname': 'Test Location',
            'address': '123 Test Address',
            'city': 'Test City'
        }[k]

        command = CreateLocationCommand(
            locationname='Test Location',
            address='123 Test Address',
            city='Test City'
        )

        location = Location(
            locationname='Test Location',
            address='123 Test Address',
            city='Test City'
        )

        self.mock_repository.location_exists.return_value = False
        self.mock_repository.create.return_value = location

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertIsInstance(result.value, dict)
        self.assertEqual(result.value['locationname'], 'Test Location')
        self.assertEqual(result.value['address'], '123 Test Address')
        self.assertEqual(result.value['city'], 'Test City')
        self.mock_repository.location_exists.assert_called_once_with('Test Location')
        self.mock_repository.create.assert_called_once_with(mock_validated_data)

    @patch('core.serializers.location.create_location_cmd_serializer.CreateLocationCommandSerializer.is_valid',
           return_value=False)
    @patch('core.serializers.location.create_location_cmd_serializer.CreateLocationCommandSerializer.errors',
           new_callable=MagicMock)
    def test_handle_given_invalid_command_should_return_validation_error(self, mock_errors, mock_is_valid):
        # Arrange
        mock_errors.return_value = {'error': 'Invalid data'}

        command = CreateLocationCommand(
            locationname='Invalid Location',
            address='',
            city=''
        )

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, mock_errors)
        self.mock_repository.location_exists.assert_not_called()
        self.mock_repository.create.assert_not_called()

    @patch('core.serializers.location.create_location_cmd_serializer.CreateLocationCommandSerializer.is_valid', return_value=True)
    @patch('core.serializers.location.create_location_cmd_serializer.CreateLocationCommandSerializer.validated_data', new_callable=MagicMock)
    def test_handle_given_existing_location_should_return_already_exists_error(self, mock_validated_data,
                                                                               mock_is_valid):
        # Arrange
        mock_validated_data.__getitem__.side_effect = lambda k: {
            'locationname': 'Existing Location',
            'address': '456 Test Address',
            'city': 'Test City'
        }[k]

        command = CreateLocationCommand(
            locationname='Existing Location',
            address='456 Test Address',
            city='Test City'
        )

        self.mock_repository.location_exists.return_value = True

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, 'A player with this Existing Location already exists.')
        self.mock_repository.location_exists.assert_called_once_with('Existing Location')
        self.mock_repository.create.assert_not_called()


