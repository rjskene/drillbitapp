from django.apps import AppConfig

btc = None

class EnvironmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'environment'

    def ready(self):
        from drillbit import BitcoinEnvironmentUtility
        
        global btc
        btc = BitcoinEnvironmentUtility()
        