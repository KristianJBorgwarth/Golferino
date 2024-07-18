import os
import unittest

from parameterized import parameterized

import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.serializers.player.create_player_cmd_serializer import CreatePlayerCommandSerializer


class TestCreatePlayerCommandSerializer(unittest.TestCase):

    def test_valid_data(self):
        # Arrange
        data = {
            'firstname': 'TestFirstName',
            'lastname': 'TestLastName',
            'email': 'Test@mail.com'
        }
        serializer = CreatePlayerCommandSerializer(data=data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertTrue(is_valid)
        self.assertEqual(serializer.validated_data, data)

    @parameterized.expand([
        ('missing_firstname',
         {'lastname': 'TestLastName', 'email': 'Test@mail.com'},
         'firstname'),

        ('empty_firstname',
         {'firstname': '', 'lastname': 'TestLastName', 'email': 'Test@mail.com'},
         'firstname'),

        ('invalid_firstname_non_alpha',
         {'firstname': 'TestFirstName123',
          'lastname': 'TestLastName',
          'email': 'Test@mail.com'},
         'firstname'),

        ('firstname_too_short',
         {'firstname': 'T', 'lastname': 'TestLastName', 'email': 'Test@mail.com'},
         'firstname'),

        ('invalid_lastname_too_short',
         {'firstname': 'TestFirstName', 'lastname': 'T', 'email': 'Test@mail.com'},
         'lastname'),

        ('invalid_email_no_at',
         {'firstname': 'TestFirstName', 'lastname': 'TestLastName', 'email': 'Testmail.com'},
         'email'),

        ('invalid_city_too_short',
         {'firstname': 'TestFirstName', 'lastname': 'TestLastName', 'email': 'C'},
         'email'),
    ])
    def test_invalid_data(self, name, data, error_field):
        # Arrange
        serializer = CreatePlayerCommandSerializer(data=data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn(error_field, serializer.errors)
