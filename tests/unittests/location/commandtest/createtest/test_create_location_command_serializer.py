import os
import unittest

from parameterized import parameterized
import django

# Ensure the DJANGO_SETTINGS_MODULE is set to your project's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Golferino.settings'
django.setup()

from core.serializers.location.create_location_cmd_serializer import CreateLocationCommandSerializer


class TestCreateLocationCommandSerializer(unittest.TestCase):

    def test_valid_data(self):
        # Arrange
        data = {
            'locationname': 'TestLocation',
            'address': '123 Test Address',
            'city': 'TestCity'
        }
        serializer = CreateLocationCommandSerializer(data=data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertTrue(is_valid)
        self.assertEqual(serializer.validated_data, data)

    @parameterized.expand([
        ('missing_locationname', {'address': '123 Test Address', 'city': 'TestCity'}, 'locationname'),
        ('empty_locationname', {'locationname': '', 'address': '123 Test Address', 'city': 'TestCity'}, 'locationname'),
        ('invalid_locationname_non_alpha', {'locationname': 'Test123', 'address': '123 Test Address', 'city': 'TestCity'}, 'locationname'),
        ('invalid_locationname_too_short', {'locationname': 'T', 'address': '123 Test Address', 'city': 'TestCity'}, 'locationname'),
        ('invalid_address_too_short', {'locationname': 'TestLocation', 'address': '123', 'city': 'TestCity'}, 'address'),
        ('invalid_city_non_alpha', {'locationname': 'TestLocation', 'address': '123 Test Address', 'city': 'City123'}, 'city'),
        ('invalid_city_too_short', {'locationname': 'TestLocation', 'address': '123 Test Address', 'city': 'C'}, 'city'),
    ])
    def test_invalid_data(self, name, data, error_field):
        # Arrange
        serializer = CreateLocationCommandSerializer(data=data)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn(error_field, serializer.errors)
