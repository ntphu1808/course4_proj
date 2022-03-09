"""
define celery_app as part of the __all__ contents of the project model. 
This will allow Celery to find the app variable by importing celery_app from the Django project and allow us 
to use a special shared_task decorator.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
