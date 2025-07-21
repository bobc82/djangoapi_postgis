# django_postgis

The following Django api contains both rest endpoints and template endpoint with map template using this framework 
for some examples: https://leafletjs.com

# Little generic concepts for Django

To create new empty Django project you can write at the prompt:

```
django-admin startproject djangoapi_postgis
```

To create new app (that can contains some endpoint to a table), you can use:

```
python manage.py startapp neighborhoods
```

After you have to add this app into INSTALLED_APPS in settings.py file

In settings.py file is configured the dababase connection to nyc database in localhost. This user is postgres and password is admin.
Sample database is taken from: https://postgis.net/workshops/postgis-intro/loading_data.html

To implement Django rest api you have to install rest_framework_gis and GeoDjango and adding these to INSTALLED_APPS.

```
pip install djangorestframework-gis

INSTALLED_APPS = [...
    'django.contrib.gis',
    'rest_framework_gis',
    ...
];
```

models.py contains the GeoDjango models that natively support PostgreSql and PostGIS. Under neighborhoods/models.py there is the model 
of nyc_neighborhood table. Normally, you have to run migration, if the database is empty with the following command:

```
python manage.py makemigrations neighborhoods
python manage.py migrate
```

Note that, if table exists, you don't need to run the second command migrate, but in this case you have to create django_ession manually into the db.
You should run this command:

```
python manage.py sqlmigrate sessions 0001
```

And execute the resulting SQL in you local database.

In the main django_postgis/urls.py you can view endpoints of these django API.

To read data we added Serialized model (i.e. under NycNeighborhood there is the NycNeighborhoodSerializer). In NycNeighborhoodSerialized
there is an adding field, that we named geom. This is useful to trasform data from geometry type in geography type (later we'll see that
this will be useful to represent coordinates with couples of "latitude,longitude" for example to prepare data for insert to a map).

# Execution of Django Api

You could try to run djando api and execute a rest endpoint via Postman:

```
python manage.py runserver
```

To get all neighborhoods, you can execute on Postman:

```
GET http://localhost:8000/neighborhoods/
```

Furthermore are some examples using template mapping with Leafletjs. For example, you could open your browser and run:

```
http://localhost:8000/map/neigh/1
```

And you can see the first neighborhood contained in nyc_neighborhoods table mapped.