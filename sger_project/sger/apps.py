from django.apps import AppConfig


class SgerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sger'

    def ready(self):
        import sger.signals 
