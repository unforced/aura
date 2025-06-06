from celery import Celery
from app.core.config import settings

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

celery_app = Celery(
    "tasks",
    broker=redis_url,
    backend=redis_url
)

celery_app.conf.update(
    task_track_started=True,
)

@celery_app.task
def add(x, y):
    return x + y 