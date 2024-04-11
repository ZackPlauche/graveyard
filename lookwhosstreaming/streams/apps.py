from django.apps import AppConfig
from logging import getLogger

class StreamsConfig(AppConfig):
    name = 'streams'
    
    def ready(self):
        from streams.models import Platform
        from django.conf import settings

        logger = getLogger('django')
        logger.info("Running the django startup, creating default platform models")

        for platform in settings.PLATFORMS:
            try:
                object_, created = Platform.objects.update_or_create(name = platform)
            except:
                pass
            # logger.info(f"Platform {platform} created = {created}")
            
    