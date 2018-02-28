Requirements: restframework => pip install djangorestframework
              postgresql => https://www.postgresql.org/download/
              psycopg2 => pip install psycopg2

After cloning the repo, a few edits in the settings.py file are needed to make the app work.

First, the SECRET_KEY variable has been commented out. You will need a secret key to make the app work. Create a dummy Django project
(can be named anything; we're only doing this to get a secret key. For this example, I will use the name used in the Django documentations - mysite):
https://docs.djangoproject.com/en/2.0/intro/tutorial01/

from mysite/mysite/settings.py, copy the SECRET_KEY value and save it in the settings.py file from this repo. Also uncomment the SECRET_KEY line.

then, uncomment the following section in the same file:
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '1234',
    }
}
"""

After setting up postgresql ( https://www.techrepublic.com/blog/diy-it-guy/diy-a-postgresql-database-server-setup-anyone-can-handle/ ),
enter the name of your database in 'NAME' field; username, password to connect to the DB server in 'USER', 'PASSWORD' fields. 'HOST' field can be
left empty.

Finally, delete the following line from settings.py:
from .secret_settings import *
