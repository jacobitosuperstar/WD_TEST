from django.apps import AppConfig


class PreferencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'preferences'

    def ready(self):
        from . import signals
