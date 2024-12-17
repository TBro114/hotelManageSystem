"""
WSGI config for hotelManageSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from timer_t import increment_counter
import threading


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelManageSystem.settings')

thread=threading.Thread(target=increment_counter)
thread.daemon=True
thread.start()

application = get_wsgi_application()

