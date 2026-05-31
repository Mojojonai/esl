"""
ASGI config for eslapp project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eslapp.settings')

application = get_asgi_application()
