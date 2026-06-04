from fastapi import HTTPException

class NotEnoughStock(HTTPException):
    def __init__(self, stock: int, requested: int) -> None:
        super().__init__(status_code=409, detail=f"Not enough stock. You requested - {requested}, but only {stock} available")

class ProductNotFound(HTTPException):
    def __init__(self, product_id: int) -> None:
        super().__init__(status_code=404, detail=f"Product - {product_id}-id not found.")

class UserNotActive(HTTPException):
    def __init__(self, user_id: int) -> None:
        super().__init__(status_code=403, detail=f"User - {user_id} is not active or does not exist.")

