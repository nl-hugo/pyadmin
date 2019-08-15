





# deploy to heroku

## commit
heroku app is linked to git repo with automatic deploys enabled

    git add .
    git commit -m 'message'
    git push origin master

on push, Heroku will pickup the latest version from the master branch and deploy


# create env and install requirements
Use pip freeze, not conda export

    pip freeze > requirements.txt



## setup django

    heroku run python manage.py migrate -a pyadmin


## create superuser
    heroku run python manage.py createsuperuser -a pyadmin


heroku logs --tail -a pyadmin



# Run tests
    python manage.py test kilometers

or single test:
    python manage.py test kilometers.tests.TripTestCase.test_update_destination


# dump data
    python manage.py dumpdata kilometers > ./kilometers/fixtures/tests.json


# load data
    python manage.py loaddata ./kilometers/fixtures/tests.json


## Run locally
    heroku local web -f Procfile.windows


# run in command line

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyadmin.settings')
django.setup()




# Update and admin commands

## makemigrations
    python manage.py makemigrations


## freeze packages
    conda env export > requirements.txt

##
    pip install -r requirements.txt


# TODO's:

- saving a location breaks if zip code does not exist
- expose driving distance API to support /distance/3512JC/3584AA/?format=json

- trips could be billable
- make monthly invoice per client, with project > activity breakdown
- invoice line items should refer to hours or trips
- rename projectHours to projectActivity/product?
- rename activity to product?


