import os
from pathlib import Path

import speckenv
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise


BASE_DIR = Path(__file__).resolve().parent

speckenv.read_speckenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmmoney.settings")
application = get_wsgi_application()
application = WhiteNoise(application)
# TODO immutable_file_test=r"\.[0-9a-f]{12,20}\..+$"
application.add_files(BASE_DIR / "static", "/static/")


class Middleware:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        iterable = None
        try:
            iterable = self.application(environ, start_response)
            yield from iterable
        finally:
            if hasattr(iterable, "close"):
                iterable.close()


application = Middleware(application)
