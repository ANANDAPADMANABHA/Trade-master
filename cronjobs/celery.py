# celery_config.py
from celery import Celery
from celery.schedules import crontab

app = Celery('trade_tasks', broker='redis://localhost:6379/0')


app.conf.update(
    timezone='Asia/Calcutta',  # Set your local timezone here
    enable_utc=True,  # Ensure UTC is enabled
)
app.autodiscover_tasks(['cronjobs'])

app.conf.beat_schedule = {
    'run-trade-task-every-morning': {
        'task': 'cronjobs.tasks.run_trade_task',
        'schedule': crontab(minute=20, hour=9, day_of_week='mon-fri'),
    },
}
