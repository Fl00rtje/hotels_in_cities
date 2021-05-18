from django.db import models


class City(models.Model):
    """The city model holds information related to the cities."""
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Hotel(models.Model):
    """
        The hotel model holds information related to the hotels.
        Each hotel has a foreign key to the city the hotel is in.
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    code = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
