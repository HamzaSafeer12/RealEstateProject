from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealEstate.settings')

app = Celery('RealEstate')  # Apne project ka naam yahan likhein
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Karachi')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
