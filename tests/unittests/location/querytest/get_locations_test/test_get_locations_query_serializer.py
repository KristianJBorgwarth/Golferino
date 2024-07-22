
import unittest
from parameterized import parameterized
from core.serializers.location.get_locations_query_serializer import GetLocationsQuerySerializer


class TestGetLocationsQuerySerializer(unittest.TestCase):
    
    def test_valid_data(self):
        # Arrange
        data = {
            'page': 1,
            'page_size': 1
        }
        serializer = GetLocationsQuerySerializer(data=data)
        
        # Act
        is_valid = serializer.is_valid()
        
        # Assert
        self.assertTrue(is_valid)
        self.assertEqual(serializer.validated_data, data)

    @parameterized.expand([
        ('invalid_page', {'page': -1, 'page_size': 1}, 'page'),
        ('invalid_page_size', {'page': 1, 'page_size': 0}, 'page_size'),
        ('invalid_page_and_page_size', {'page': -1, 'page_size': 0}, 'page'),
    ])
    def test_invalid_data(self, name, data, error_field):
        # Arrange
        serializer = GetLocationsQuerySerializer(data=data)
        
        # Act
        is_valid = serializer.is_valid()
        
        # Assert
        self.assertFalse(is_valid)
        self.assertIn(error_field, serializer.errors)
        