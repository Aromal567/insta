import os
import sys

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTER_DIR = os.path.dirname(BASE_DIR)

# Make sure Django can find myapp
sys.path.append(BASE_DIR)     # inner myproject
sys.path.append(OUTER_DIR)    # outer folder

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.myproject.settings")

application = get_wsgi_application()
