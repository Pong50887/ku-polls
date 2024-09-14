"""Polls application configuration for the Django project."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
        Configuration class for the Polls application. Sets the default
        auto field and the application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
