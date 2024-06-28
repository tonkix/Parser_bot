import logging
import random
from app.db.models import async_session
from app.db.models import User, Product, Link
from sqlalchemy import select


async def set_user(tg_id, firstname, lastname, subscribed, role=1):
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


async def get_user_by_tg(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user_by_id(id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == id))


async def subscribe(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User)
                                       .order_by(User.id)
                                       .where(User.tg_id==tg_id)
                                       .limit(1))
        user = result.scalar()
        user.subscribed = True
        await session.commit()


async def unsubscribe(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User)
                                       .order_by(User.id)
                                       .where(User.tg_id==tg_id)
                                       .limit(1))
        user = result.scalar()
        user.subscribed = False
        await session.commit()


async def add_link(url, price, name, product_id):
    async with async_session() as session:
        links = await session.scalars(select(Link).where(Link.url == url))
        for link in links:
            if product_id == link.product_id:
                return

        session.add(Link(
                url=url,
                price=price,
                name=name,
                product_id=product_id))
        logging.info(f"Добавлена запись в 'links' - {product_id} {url} {price}")
        await session.commit()


async def get_links_by_tt_id(product_tt_id):
    async with async_session() as session:
        return await session.scalars(select(Link).where(Link.product_id == product_tt_id))


async def get_subscribed_users():
    async with async_session() as session:
        return await session.scalars(select(User).where(User.subscribed == 1))