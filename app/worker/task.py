import asyncio
from sqlalchemy import update
from app.celery import celery_app
from app.session import session_factory
from app.db import Product

@celery_app.task()
