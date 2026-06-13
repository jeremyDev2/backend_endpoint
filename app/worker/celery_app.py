from celery import Celery
from app.settings import settings

celery_app = Celery("worker", broker=str(settings.amqp_dns))
