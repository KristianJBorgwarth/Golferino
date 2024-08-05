import os

import django
# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

import unittest
from unittest.mock import MagicMock
from core.commands.location.create.create_location_command import CreateLocationCommand
from core.commands.location.create.create_location_command_handler import CreateLocationCommandHandler
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository


class TestCreateLocationCommandHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=LocationRepository)
        self.handler = CreateLocationCommandHandler()
        self.handler.location_repository = self.mock_repository

    def test_handle_given_valid_command_should_create_and_return_result_ok_LocationDto(self):
        # Arrange
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
        self.mock_repository.create_2.return_value = location

        # Act
        result = self.handler.handle(command)

        # Assert
        self.assertTrue(result.is_success)
        self.assertIsInstance(result.value, dict)
        self.assertEqual(result.value['locationname'], 'Test Location')
        self.assertEqual(result.value['address'], '123 Test Address')
        self.assertEqual(result.value['city'], 'Test City')
        self.mock_repository.location_exists.assert_called_once_with(location_name='Test Location')
        self.mock_repository.create_2.assert_called()

    def test_handle_given_existing_location_should_return_already_exists_error(self):
        # Arrange
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
        self.mock_repository.location_exists.assert_called_once_with(location_name='Existing Location')
        self.mock_repository.create_2.assert_not_called()

