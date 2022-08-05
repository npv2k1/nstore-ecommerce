from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nstore.core'
    def ready(self) -> None:
        import nstore.core.signals.handlers