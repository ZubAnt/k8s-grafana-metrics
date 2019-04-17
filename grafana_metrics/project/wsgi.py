import os

from django.core.wsgi import get_wsgi_application


env = os.getenv('ENV', 'base')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'grafana_metrics.project.settings.{env}')

application = get_wsgi_application()
