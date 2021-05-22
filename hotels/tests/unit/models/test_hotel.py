from django.test import TestCase
from hotels.models import City, Hotel


class HotelTest(TestCase):
    def setUp(self):
        amsterdam = City.objects.create(code="AMS", name="Amsterdam")
        Hotel.objects.create(city=amsterdam, code="AMS01", name="Ibis")

    def test_create_hotel(self):
        """Created hotel has the city, code and name that belongs to the hotel."""
        amsterdam = City.objects.get(name="Amsterdam")
        ibis = Hotel.objects.get(name="Ibis")

        self.assertEqual(ibis.city, amsterdam)
        self.assertEqual(ibis.code, "AMS01")
        self.assertEqual(ibis.name, "Ibis")