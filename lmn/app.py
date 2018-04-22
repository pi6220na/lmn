from django.apps import AppConfig


class LmnConfig(AppConfig):
    name = 'LMN'
    verbose_name = 'LMN App Config'

    def ready(self):
        import app.lmn.lmn.signals
