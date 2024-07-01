import logging
from app.db.models import async_session
from app.db.models import User, Product, Link
from sqlalchemy import select
from datetime import datetime


async def set_user(tg_id: int, firstname, lastname, subscribed, role=1):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             firstname=firstname,
                             lastname=lastname,
                             subscribed=subscribed,
                             role=role))
            await session.commit()


async def check_password(password):
    return password == '41802967'


async def get_user_by_tg(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user_by_id(user_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == user_id))


async def subscribe(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User)
                                       .order_by(User.id)
                                       .where(User.tg_id == tg_id)
                                       .limit(1))
        user = result.scalar()
        user.subscribed = True
        await session.commit()


async def unsubscribe(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User)
                                       .order_by(User.id)
                                       .where(User.tg_id == tg_id)
                                       .limit(1))
        user = result.scalar()
        user.subscribed = False
        await session.commit()


async def add_link(url, price, name, product_id):
    async with async_session() as session:
        links = list(await session.scalars(select(Link).where(Link.url == url)))
        if len(links) == 0:
            session.add(Link(
                url=url,
                price=price,
                name=name,
                product_id=product_id))
            logging.info(f"Добавлена запись в 'links' - {product_id} {url} {price}")
        else:
            for link in links:
                if product_id == link.product_id:
                    logging.info(f"Такая запись уже существует 'links' - {product_id} {url} {price}")
                    continue
                else:
                    session.add(Link(
                        url=url,
                        price=price,
                        name=name,
                        product_id=product_id))
                    logging.info(f"Добавлена запись в 'links' - {product_id} {url} {price}")
        await session.commit()


async def get_product_by_tt_id(product_tt_id):
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.product_tt_id == product_tt_id))
        return product


async def get_product_by_tt_code(product_tt_code):
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.product_tt_code == product_tt_code))
        return product


async def get_links_by_tt_id(product_tt_id):
    async with async_session() as session:
        return await session.scalars(select(Link).where(Link.product_id == product_tt_id))


async def get_links_by_tt_code(product_tt_code):
    async with async_session() as session:
        product = await get_product_by_tt_code(product_tt_code)
        return await session.scalars(select(Link).where(Link.product_id == product.product_tt_id))


async def get_subscribed_users():
    async with async_session() as session:
        return await session.scalars(select(User).where(User.subscribed == 1))


async def add_tt_product(product_tt_id, product_tt_code, name, url, purchase_price, retail_price):
    async with async_session() as session:
        links = list(await session.scalars(select(Link).where(Link.url == url)))
        if not links:
            session.add(Product(
                product_tt_id=product_tt_id,
                product_tt_code=product_tt_code,
                name=name,
                url=url,
                purchase_price=purchase_price,
                retail_price=retail_price,
                update_date=datetime.now()))
            logging.info(f"Добавлена запись в 'products' - {product_tt_id} --- {url} --- "
                         f"Закуп {purchase_price} / Розница {retail_price}")
            await session.commit()
        else:
            logging.info(f"Такая запись уже существует 'products' - {product_tt_id} {url}")
            return
