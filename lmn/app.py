from django.apps import AppConfig


class LmnConfig(AppConfig):
    name = 'LMN'
    verbose_name = 'LMN App Config'

    def ready(self):
        import lmn.lmn.signals
