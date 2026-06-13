import asyncio
import celery_app
from sqlalchemy import update
from app.session import session_factory
from app.db import Product

@celery_app.task(name="sync_stock_to_db")
def sync_stock_to_db(product_id: int, purchased_count: int) -> None:
    asyncio.run(_sync(product_id, purchased_count))

async def _sync(product_id: int, purchased_count: int) -> None:
    async with session_factory() as session:
        stmt = (update(Product)
                .where(Product.product_id == product_id)
                .values(stock=Product.stock - purchased_count)
                )
        await session.execute(stmt)
        await session.commit()
