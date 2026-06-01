from pydantic import BaseModel, Field

class PurchaseRequest(BaseModel):

    user_id: int = Field(..., gt=0, description="User ID of the purchaser")
    product_id: int = Field(..., gt=0, description="ID of the purchased product")
    purchased_count: int = Field(..., gt=0, description="Number of items purchased")

class PurchaseResponse(BaseModel):

    status: str = Field(..., description="Purchase Status")
