from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
from django.conf import settings
from celery.schedules import crontab
from celery.schedules import timedelta
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    print('hello world')


# app.conf.update(
#     CELERYBEAT_SCHEDULE = {
#         'fetch-nba-news-every-hour': { 
#             'task': 'crawler.tasks.get_nba_news',
#             'schedule': 60.0,
#             'args': ()
#         }
#     }
# )
app.conf.update(
    beat_schedule = {
        'fetch-nba-news-every-hour': { 
            'task': 'get_nba_news',
            'schedule': crontab(minute=0, hour='*/1'),
            # 'schedule': timedelta(seconds=60),
            'args': ()
        }
    }
)