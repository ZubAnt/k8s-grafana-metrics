import os

from django.core.wsgi import get_wsgi_application


env = os.getenv('ENV', 'base')

application = get_wsgi_application()
