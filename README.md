# metarita

An [APISbaseproject](https://github.com/acdh-oeaw/apisbaseproject) clone to caputure metadata about inventories transcribed in the project 'Reading in the Alps'


Installation
------------

* clone the repo :code:`git clone https://github.com/acdh-oeaw/apisbaseproject.git <folder-name>`
* customize :code:`webpage.metadata`,
* recommended: create a virtual environment
* install requirements :code:`pip install -r requirements.txt`
* in :code:`webpage/static/webpage/libraries` run :code:`bower install`
* before you can run the inital migrations
    * first run :code:`python manage.py delete_migrate --settings=apis.settings.<custom settings file>` to delete any existing migration files.
    * :code:`python manage.py migrate --settings=apis.settings.<custom settings file>` this will create django's default database tables
    * :code:`python manage.py makemigrations --settings=apis.settings.<custom settings file>` this will cretae the migration files for the apis-specific applications.
    * :code:`python manage.py migrate --settings=apis.settings.<custom settings file>` and this will create the according data base tables
* in :code:`apis.urls` UNcomment the commentented the items in the code:`urlpatterns` list
* start the dev-server :code:`python manage.py runserver --settings=apis.settings.<custom settings file>`
