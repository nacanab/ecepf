from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Importez les signaux ici