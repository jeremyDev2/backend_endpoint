import asyncio
from app.worker.celery_app import celery_app
from sqlalchemy import update
from app.session import session_factory
from app.db import Product
import threading
from celery.signals import worker_process_init, worker_process_shutdown

loop = asyncio.new_event_loop()

@worker_process_init.connect
def __start_loop(**kwargs):
    threading.Thread(target=loop.run_forever, daemon=True).start()

@worker_process_shutdown.connect
def stop_loop(**kwargs):
    loop.call_soon_threadsafe(loop.stop)

@celery_app.task(name="sync_stock_to_db")
def sync_stock_to_db(product_id: int, purchased_count: int) -> None:
    future = asyncio.run_coroutine_threadsafe(_sync(product_id, purchased_count), loop=loop)
    return future.result()


async def _sync(product_id: int, purchased_count: int) -> None:
    async with session_factory() as session:
        stmt = (update(Product)
                .where(Product.product_id == product_id)
                .values(stock=Product.stock - purchased_count)
                )
        await session.execute(stmt)
        await session.commit()
