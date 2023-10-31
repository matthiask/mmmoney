import os

import speckenv
from django.core.wsgi import get_wsgi_application


speckenv.read_speckenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmmoney.settings")
application = get_wsgi_application()
