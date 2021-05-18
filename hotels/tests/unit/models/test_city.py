from unittest import TestCase
from assignment.hotels.models import City
# some more settings to make the test actually run ;)


class CityTest(TestCase):
    def test_create_city(self):
        c = City('AMS', 'Amsterdam')

        self.assertEqual(c.code, 'AMS')
        self.assertEqual(c.name, 'Amsterdam')

