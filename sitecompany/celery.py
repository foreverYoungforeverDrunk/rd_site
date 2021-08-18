import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitecompany.settings')
app = Celery('sitecompany')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'payroll_every_2_hours': {
        'task': 'workers.tasks.payroll',
        # 'schedule': crontab(minute='*/2'),
        'schedule': crontab(hour='*/2'),
    },
}
