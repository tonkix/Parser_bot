from datetime import datetime
from sqlalchemy import BigInteger, String, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    subscribed: Mapped[bool]
    role: Mapped[int]


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_tt_id: Mapped[int] = mapped_column(Integer, nullable=True)
    product_tt_code: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(250), nullable=True)
    url: Mapped[str] = mapped_column(String(500), nullable=True)
    purchase_price: Mapped[int] = mapped_column(Integer, nullable=True)
    retail_price: Mapped[int] = mapped_column(Integer, nullable=True)
    update_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime)

    '''def __iter__(self):
        return [self.id,
                self.product_tt_id,
                self.product_tt_code,
                self.name,
                self.url,
                self.purchase_price,
                self.retail_price,
                self.update_date]'''

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Link(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500))
    price: Mapped[int]
    name: Mapped[str] = mapped_column(String(250))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_tt_id'))


class Change(Base):
    __tablename__ = 'changes'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    update_date: Mapped[datetime]
    purchase_price: Mapped[int]
    retail_price: Mapped[int]


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
