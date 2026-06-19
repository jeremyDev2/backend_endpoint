from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): pass

# Postgres — постоянное хранилище остатков товаров.
# Во время работы приложения актуальный счётчик хранится в Redis;
# Postgres обновляется асинхронно Celery-воркером после каждой успешной покупки.
class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    stock: Mapped[int]
    description: Mapped[str]
