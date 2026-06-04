from fastapi import APIRouter
from app.schemas import PurchaseRequest, PurchaseResponse
from app.db import repository
from app.exceptions.exceptions import NotEnoughStock

router = APIRouter()

@router.post("/purchase")
async def purchase(request:PurchaseRequest) -> PurchaseResponse:
    success:bool = await repository.purchase(request)
    if not success:
        raise NotEnoughStock(stock=0, requested=request.purchased_count)
    return PurchaseResponse(status="success")
