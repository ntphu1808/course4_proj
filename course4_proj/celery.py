import os

from celery import Celery
from django.conf import settings


#set up the environment variables for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course4_proj.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev") 

import configurations

configurations.setup() #run this in order to enable Django Configurations

#instaniate a Celery object with the project name
app = Celery("course4_proj") 

#load the settings from the settings variable in django.conf module,
# then prefix Celery settings with CELERY, e.g. broker_url comes from CELERY_BROKER_URL
app.config_from_object("django.conf:settings", namespace="CELERY")

# Go through INSTALLED_APPS and looks inside tasks.py and models.py.
# and load any tasks it finds.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)