from django.apps import AppConfig


class FilmsConfig(AppConfig):
    name = "films"

    def ready(self):
        from films import signals
