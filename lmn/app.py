from django.apps import AppConfig


class LmnConfig(AppConfig):
    name = 'LMNOP'
    verbose_name = 'LMNOP App Config'

    def ready(self):
        import app.lmn.lmn.signals
