from django.apps import AppConfig


class AuctionsConfig(AppConfig):
    # https://stackoverflow.com/questions/67783120/warning-auto-created-primary-key-used-when-not-defining-a-primary-key-type-by
    default_auto_field = 'django.db.models.AutoField'
    
    name = 'auctions'
