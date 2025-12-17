import os
import logging
from app.db.models import async_session
from app.db.models import User, Product, Link
from sqlalchemy import select
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")


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
    return password == MASTER_PASSWORD


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
        links = await session.scalars(select(Link).where(Link.url == url))
        for link in links:
            if product_id == link.product_id:
                logging.info(f"Такая запись уже существует 'links' - {product_id} {url} {price}")
                return
        session.add(Link(
            url=url,
            price=price,
            name=name,
            product_id=product_id))
        logging.info(f"Добавлена запись в 'links' - {product_id} {url} {price}")
        await session.commit()


async def get_product_by_tt_id(product_tt_id: int):
    async with async_session() as session:
        products = await session.scalars(select(Product).where(Product.product_tt_id == product_tt_id))
        # print('[INFO] ищу по ID')
        return products


async def get_product_by_tt_code(product_tt_code: int):
    async with async_session() as session:
        products = await session.scalars(select(Product).where(Product.product_tt_code == product_tt_code))
        # print('[INFO] ищу по Code')
        return products


async def get_products_by_link(url):
    async with async_session() as session:
        links = await session.scalars(select(Link).where(Link.url == url))
        products_tt = list(await session.scalars(select(Product).where(Product.url == url)))
        for link in links:
            product = await get_product_by_tt_id(link.product_id)
            products_tt.append(product)
        # print('[INFO] ищу по URL')
        return products_tt


# Поиск по полному совпадению имени
async def get_products_by_name(name: str):
    async with async_session() as session:
        name = name.lower().split(' ')
        # print(name)
        out_products = list()
        for word in name:
            products_tt = await session.scalars(select(Product).where(Product.name.contains(word)))
            for p in products_tt:
                out_products.append(p)
        # print('[INFO] ищу по NAME')
        return out_products


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


async def add_tt_product2(**kwargs):
    async with async_session() as session:
        links = list(await session.scalars(select(Link).where(Link.url == kwargs['url'])))
        if not links:
            try:
                session.add(Product(
                    product_tt_id=kwargs['product_tt_id'],
                    product_tt_code=kwargs['product_tt_code'],
                    name=kwargs['name_tt'] if kwargs['name_tt'] is not None else "",
                    url=kwargs['url_tt'] if kwargs['url_tt'] is not None else "",
                    purchase_price=kwargs['purchase_price_tt'] if kwargs['purchase_price_tt'] is not None else 0,
                    retail_price=kwargs['retail_price_tt'] if kwargs['retail_price_tt'] is not None else 0,
                    update_date=datetime.now()))
                logging.info(f"Добавлена запись в 'products' - {kwargs['product_tt_id']} --- {kwargs['url_tt']} ---"
                             f"Закуп {kwargs['purchase_price_tt']} / Розница {kwargs['retail_price_tt']}")
                await session.commit()
            except Exception as err:
                logging.error(f"Unexpected {err}")
        else:
            logging.info(f"Такая запись уже существует 'products' - {kwargs['product_tt_id']}")
            return


async def update_product2(**kwargs):
    async with async_session() as session:
        product = (await session.execute(select(Product)
                                         .where(Product.product_tt_id == kwargs['product_tt_id'])
                                         .limit(1))).scalar()
        if product is not None:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
                    # print(key, value)
                    product.update_date = datetime.now()
            logging.info('Товар обновлен')
            print('Товар обновлен')
        else:
            await add_tt_product2(**kwargs)
            print('Добавлен товар')
            logging.info('Добавлен товар из обновления')

        await session.commit()


'''async def add_tt_product(product_tt_id, product_tt_code, name, url, purchase_price, retail_price):
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
            return'''

'''async def update_product(product_tt_id, product_tt_code, name, purchase_price, retail_price):
    async with async_session() as session:
        result = await session.execute(select(Product)
                                       .where(Product.product_tt_id == product_tt_id)
                                       .limit(1))
        product = result.scalar()
        product.product_tt_code = product_tt_code
        product.name = name
        product.purchase_price = purchase_price
        product.retail_price = retail_price
        product.update_date = datetime.now()
        await session.commit()'''
