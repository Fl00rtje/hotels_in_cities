from django.test import TestCase
from requests.auth import HTTPBasicAuth
from utils import import_data
from unittest.mock import patch
import os
import pandas as pd
from hotels.models import City


class ImportDataTest(TestCase):
    def setUp(self):
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        data_path_cities = os.path.join(THIS_DIR, 'city.csv')
        data_path_hotels = os.path.join(THIS_DIR, 'hotel.csv')

        try:
            self.df_cities = pd.read_csv(f'{data_path_cities}',
                                         header=None,
                                         delimiter=";")
            self.df_hotels = pd.read_csv(f'{data_path_hotels}',
                                         header=None,
                                         delimiter=";")
            with open(data_path_cities, 'r') as file_cities:
                self.data_cities = file_cities.read()
            with open(data_path_hotels, 'r') as file_hotels:
                self.data_hotels = file_hotels.read()

        except IOError:
            print('Unable to open file')

    def test_get_city_data(self):
        """
            The city URL is called with the credentials in the config file.
            I think it's better to mock the username and password.
        """

        with patch('requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = self.data_cities

            data = import_data.get_city_data()
            mocked_get.assert_called_with("http://rachel.maykinmedia.nl/djangocase/city.csv",
                                          auth=HTTPBasicAuth("python-demo", "claw30_bumps"))

            self.assertEqual(data, self.data_cities)

    def test_get_hotel_data(self):
        """
             The hotel URL is called with the credentials in the config file.
             I think it's better to mock the username and password.
        """

        with patch('requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = self.data_hotels

            data = import_data.get_hotel_data()
            mocked_get.assert_called_with("http://rachel.maykinmedia.nl/djangocase/hotel.csv",
                                          auth=HTTPBasicAuth("python-demo", "claw30_bumps"))

            self.assertEqual(data, self.data_hotels)

    def test_make_city_dataframe(self):
        """The amount of cities in the dataframe is correct."""
        result = import_data.make_city_dataframe(self.data_cities)

        self.assertEqual(len(result), len(self.df_cities.index))

    def test_make_hotel_dataframe(self):
        """The amount of hotels in the dataframe is correct."""
        result = import_data.make_hotel_dataframe(self.data_hotels)

        self.assertEqual(len(result), len(self.df_hotels.index))

    def test_create_city_objects(self):
        """Creates the city objects from the dataframe"""
        result = import_data.create_city_objects(self.df_cities)

        self.assertEqual(len(result), len(self.df_cities.index))

    def test_create_hotel_objects(self):
        """
            Creates the hotel objects from the dataframe.
            I think this can be improved, because new cities can be added
            which won't be automatically created in the tests.
        """

        City.objects.create(code="AMS", name="Amsterdam")
        City.objects.create(code="ANT", name="Antwerpen")
        City.objects.create(code="ATH", name="Athene")
        City.objects.create(code="BAK", name="Bangkok")
        City.objects.create(code="BAR", name="Barcelona")
        City.objects.create(code="BER", name="Berlijn")

        result = import_data.create_hotel_objects(self.df_hotels)

        self.assertEqual(len(result), len(self.df_hotels.index))
