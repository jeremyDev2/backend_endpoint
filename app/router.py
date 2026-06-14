from fastapi import APIRouter
from app.schemas import PurchaseRequest, PurchaseResponse
from app.db import repository
from app.exceptions.exceptions import NotEnoughStock, ProductNotFound

router = APIRouter()

@router.post("/purchase")
async def purchase(request:PurchaseRequest) -> PurchaseResponse: 
    res: int = await repository.purchase_redis(request)

    if res == -2:
        raise ProductNotFound(request.product_id)
    if res == -1:
        raise NotEnoughStock(stock=0, requested=request.purchased_count)

    return PurchaseResponse(status="success")
