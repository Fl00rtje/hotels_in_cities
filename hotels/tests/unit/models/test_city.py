from django.test import TestCase
from hotels.models import City


class CityTest(TestCase):
    def setUp(self):
        City.objects.create(code="AMS", name="Amsterdam")

    def test_create_city(self):
        """Created city has the city code and name that belongs to them."""
        amsterdam = City.objects.get(name="Amsterdam")

        self.assertEqual(amsterdam.code, 'AMS')
        self.assertEqual(amsterdam.name, 'Amsterdam')

