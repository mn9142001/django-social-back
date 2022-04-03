import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root="/staticfiles")
