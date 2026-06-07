import asyncio
from sqlalchemy import insert
from app.session import session_factory
from app.db.db import Product
from app.data import products

async def seed():
    async with session_factory() as session:
        await session.execute(insert(Product).values(products))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
