from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.session import session_factory
from app.db import Product
from app.cache.redis_client import redis_client
from app.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with session_factory() as session:
        res = await session.execute(select(Product))
        products = res.scalars().all()

    async with redis_client.pipeline() as pipe:
        for product in products:
            pipe.set(f"stock:{product.product_id}", product.stock)
        await pipe.execute()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
