from sqlalchemy import update
from app.schemas import PurchaseRequest
from app.session import session_factory

async def purchase(request: PurchaseRequest) -> bool:
    async with session_factory() as session:
        stmt = (update(Product)
                .where(Product.product_id == request.product_id, Product.stock >= request.purchased_count)
                .values(stock = Product.stock - request.purchased_count)
                .returning(Product.stock)
                )


        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone() is not None
