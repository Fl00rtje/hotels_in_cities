"""
    This file downloads cities and hotels over HTTP
    and saves the cities and hotels to the database.
"""

import os
import sys
import django
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from io import StringIO
from datetime import datetime

sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'assignment.settings'
django.setup()

from hotels.models import City, Hotel
from conf import credentials


def get_city_data():
    """Retrieves the city data through the URL over HTTP"""
    data = requests.get(credentials["url_cities"],
                        auth=HTTPBasicAuth(credentials["username"],
                                           credentials["password"]))

    if data.ok:
        return data.text
    else:
        return 'Bad Response'


def get_hotel_data():
    """Retrieves the hotel data through the URL over HTTP"""
    url_hotels = credentials["url_hotels"]
    data = requests.get(url_hotels, auth=HTTPBasicAuth(credentials["username"], credentials["password"]))

    if data.ok:
        return data.text
    else:
        return 'Bad Response'


def make_city_dataframe(city_data):
    """Makes a city dataframe from the obtained data through the URL."""
    dataframe = pd.read_csv(StringIO(city_data), header=None, delimiter=";")
    return dataframe


def make_hotel_dataframe(hotel_data):
    """
        Makes a hotel dataframe from the obtained data through the URL.
        There seem to be some duplicates in the hotel data, but it could also be different locations.
        For now I assumed it's different locations from a hotel chain in one city.
        If not so, duplicates could easily be removed with pandas.
    """
    dataframe = pd.read_csv(StringIO(hotel_data), header=None, delimiter=";")
    return dataframe


def create_city_objects(df_cities):
    """Creates the city objects from the dataframe"""
    cities_created = [
        City(
            code=row[0],
            name=row[1]
        )
        for index, row in df_cities.iterrows()
    ]

    return cities_created


def create_hotel_objects(df_hotels):
    """
        Creates the hotel objects from the dataframe.
    """

    hotels_created = [
        Hotel(
            city=City.objects.get(code=row[0]),
            code=row[1],
            name=row[2]
        )
        for index, row in df_hotels.iterrows()
    ]

    return hotels_created


def add_cities_to_db(cities):
    """
        Deletes first the cities from the database and afterwards adds the new cities.
        This could be changed / improved by checking by the city code:
        - if the city is not in the dataframe, delete the city from the database
        - if the city is in de db already, update the record (by update_or_create I think)
    """
    City.objects.all().delete()
    City.objects.bulk_create(cities)
    print(f"Added {len(cities)} cities to the database")

    # f = open(f"cities_log.txt", "a")
    # f.write(f"{datetime.now()}: Added {len(cities)} cities to the database\n")
    # f.close()


def add_hotels_to_db(hotels):
    """
        Deletes first the hotels from the database and afterwards adds the new hotels.
        This could be changed / improved by checking by the hotel code:
        - if the hotel is not in the dataframe, delete the hotel from the database
        - if the hotel is in de db already, update the record (by update_or_create I think)
    """
    Hotel.objects.all().delete()
    Hotel.objects.bulk_create(hotels)
    print(f"Added {len(hotels)} cities to the database")

    # f = open("hotels_log.txt", "a")
    # f.write(f"{datetime.now()}: Added {len(hotels)} hotels to the database\n")
    # f.close()


def run_cities():
    """
        This function is called by crontab to download the city data daily.
        If the file is run manually the function is called at the end of the file.
    """
    city_data = get_city_data()
    df_cities = make_city_dataframe(city_data)
    cities = create_city_objects(df_cities)
    add_cities_to_db(cities)


def run_hotels():
    """
        This function is called by crontab to download the hotel data daily.
        If the file is run manually the function is called at the end of the file.
    """
    hotel_data = get_hotel_data()
    df_hotels = make_hotel_dataframe(hotel_data)
    hotels = create_hotel_objects(df_hotels)
    add_hotels_to_db(hotels)


if __name__ == "__main__":
    run_cities()
    run_hotels()
