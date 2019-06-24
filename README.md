





# deploy to heroku

## commit
heroku app is linked to git repo

    git add .
    git commit -m 'message'
    git push origin master


# create env and install requirements

    conda env create -f environment.yml




# setup django



## migrate
    python manage.py migrate

## create superuser
    python manage.py createsuperuser

## run server
    python manage.py runserver




# Run tests
    python manage.py test kilometers

or single test:
    python manage.py test kilometers.tests.TripTestCase.test_update_destination


# dump data
    python manage.py dumpdata kilometers > ./kilometers/fixtures/tests.json


# load data
    python manage.py loaddata ./kilometers/fixtures/tests.json



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


# TODO's:

- saving a location breaks if zip code does not exist
- expose driving distance API to support /distance/3512JC/3584AA/?format=json


