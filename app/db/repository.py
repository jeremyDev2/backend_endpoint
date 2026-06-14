import asyncio
from app.cache.redis_client import decrement_stock
from app.schemas import PurchaseRequest
from app.worker.task import sync_stock_to_db

async def purchase_redis(request: PurchaseRequest) -> int:

    res = await decrement_stock(
        keys=[f"stock:{request.product_id}"], 
        args=[request.purchased_count],
    )
    if res >= 0:
        await asyncio.to_thread(
            sync_stock_to_db.delay(request.product_id, request.purchased_count)
        )
    return res
