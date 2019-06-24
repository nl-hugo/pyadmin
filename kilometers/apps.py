from django.apps import AppConfig


class KilometersConfig(AppConfig):
    name = 'kilometers'

    def ready(self):
        import kilometers.signals
