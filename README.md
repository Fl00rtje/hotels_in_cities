# Hotels in Cities
Welcome to the "Hotels in Cities" repository! 
This code is only meant as a reference since the source of the data is no longer available.

### The purpose
The purpose of the code is to import CSV hotel data over authenticated HTTP into a Django application.

### What does the Hotels in Cities code do?
The data consisted of a hotel CSV and a city CSV that were retrieved over authenticated HTTP.
The data is imported into the Django models and the relation between city and hotel (a hotel is in a certain city) is restored.
The csv's are set up to be downloaded daily with a cron job.
There is a view in which you can see a list of cities and when you select a city, the hotels in that city are shown.
The code is covered by unit tests.

### Where can I find what?
- An example of the csv city data: hotels/tests/unit/city.csv
- An example of the csv city data: hotels/tests/unit/hotel.csv
- The import logic: utils/import_data.py
- The template (view): hotels/templates/hotels/base.html
- The tests: hotels/tests/unit

### Running the import
The command for running the import: python import_data.py

### conf.py
The source and the credentials are stored outside this repository in a separate conf file.
This is how the conf.py file looks like:

```
credentials = {
    "username": "<username>",
    "password": "<password>",
    "url_cities": "<url_cities>",
    "url_hotels": "<url_hotels>",
    "secret_key": "<secret_key>"
}
```

