from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): pass

class Product(Base):
    
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    stock: Mapped[int]
    description: Mapped[str]
