import logging

import openpyxl
from aiogram import F, Bot, Router
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from openpyxl import Workbook

import app.db.requests as rq
from app.parser_1 import parsing, parsing_one

router = Router()
load_dotenv()


class ImportTT(StatesGroup):
    file = State()


def printSheets(sheets):
    list_of_sheets = list()
    for s in sheets:
        list_of_sheets.append(s)
        print(str(list_of_sheets.index(s)) + " | " + s)


def chooseSheet(wb):
    printSheets(wb.sheetnames)
    print('Введите индекс листа: ')
    sheet_index = input()
    ws = wb.sheetnames[int(sheet_index)]
    return ws


def tryDefaultSheetName(wb_data, name):
    try:
        return wb_data[name]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        logging.error(f"sheet name error")
        try:
            return wb_data[str(name).lower()]
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            logging.error(f"sheet name error")
            try:
                return wb_data[str(name).upper()]
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                logging.error(f"sheet name error")
                sheet = chooseSheet(wb_data)
    return wb_data[sheet]


async def find_elem_by_url(url, parsing_result):
    for e in parsing_result:
        if url == e[0]:
            return e


# inputFile - файл для парсинга
# return - Excel файл с результатами парсинга
async def Work_With_File(data: Workbook):
    default_sheet_name = "Ссылки"
    data = tryDefaultSheetName(wb_data=data, name=default_sheet_name)

    list_url = list()
    id_url_list = list()
    maxCheckRow = data.max_row + 1  # поиск ссылок в строках
    maxCheckColumn = 20  # поиск ссылок в колонках
    for col in range(0, maxCheckColumn):
        for row in range(0, maxCheckRow):
            cell_url = data.cell(row=row + 1, column=col + 1).value
            product_id = data.cell(row=row + 1, column=1).value
            if "http" in str(cell_url) and "." in str(cell_url):
                list_url.append(cell_url)
                id_url_list.append([product_id, cell_url])

    wb = Workbook()
    ws = wb.active
    ws.title = "Output data"
    uniq_url = list(set(list_url))
    parsing_result = await parsing(uniq_url, ws)
    sheet_name = 'dictionary'
    wb.create_sheet(sheet_name)
    ws = wb[sheet_name]
    for k in id_url_list:
        try:
            data = await find_elem_by_url(k[1], parsing_result)
            # print(str(k[0]) + "/" + str(k[1]))
            ws.append({1: k[0],
                       2: k[1],
                       3: data[1],
                       4: data[2]})

            await rq.add_link(product_id=k[0],
                              url=k[1],
                              name=data[1],
                              price=data[2])
        except Exception as err:
            mes = f"Unexpected {err=}, {type(err)=}"
            print(mes)
            logging.error(mes)

    return wb


@router.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(tg_id=message.from_user.id,
                      firstname=message.from_user.first_name,
                      lastname=message.from_user.last_name,
                      subscribed=0,
                      role=1)
    await message.answer("Hello!")


@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message):
    await rq.set_user(tg_id=message.from_user.id,
                      firstname=message.from_user.first_name,
                      lastname=message.from_user.last_name,
                      subscribed=1,
                      role=1)
    await rq.subscribe(tg_id=message.from_user.id)
    await message.answer("Вы подписались на рассылку")


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message):
    await rq.set_user(tg_id=message.from_user.id,
                      firstname=message.from_user.first_name,
                      lastname=message.from_user.last_name,
                      subscribed=0,
                      role=1)
    await rq.unsubscribe(tg_id=message.from_user.id)
    await message.answer("Вы отписались от рассылки")


@router.message(Command("import"))
async def cmd_import(message: Message, state: FSMContext):
    user = await rq.get_user_by_tg(message.from_user.id)
    if user.role == 99:
        await state.set_state(ImportTT.file)
        await message.answer(f"Жду файл импорта")
    else:
        await message.answer(f"У вас нет доступа для выполнения данной команды")


async def update_tt_products(data: Workbook):
    data = data.active
    products_list = list()
    products_dict = dict()
    maxCheckRow = data.max_row + 1  # поиск ссылок в строках
    for row in range(1, maxCheckRow):
        products_dict['product_tt_id'] = data.cell(row=row + 1, column=1).value
        products_dict['product_tt_code'] = data.cell(row=row + 1, column=2).value
        products_dict['name'] = data.cell(row=row + 1, column=3).value
        products_dict['purchase_price'] = data.cell(row=row + 1, column=4).value
        products_dict['retail_price'] = data.cell(row=row + 1, column=5).value
        products_dict['url'] = data.cell(row=row + 1, column=6).value
        # print(products_dict)
        # products_list.append([(k, v) for k, v in products_dict.items()])
        # products_list.append(products_dict)
        products_list.append([products_dict['product_tt_id'],
                              products_dict['product_tt_code'],
                              products_dict['name'],
                              products_dict['purchase_price'],
                              products_dict['retail_price'],
                              products_dict['url']])

    return products_list


@router.message(ImportTT.file)
async def get_import_file(message: Message, state: FSMContext, bot: Bot):
    await message.answer(f"Начал работу с файлом")
    file_id = message.document.file_id
    input_directory = r'import_data/'
    if not os.path.exists(input_directory):
        os.mkdir(input_directory)
    input_name = "import.xlsx"
    input_file = input_directory + input_name
    await Bot.download(bot, file_id, input_file, 120)
    input_file = openpyxl.load_workbook(os.path.join(input_directory, input_name))
    products = await update_tt_products(input_file)
    for product in products:
        # await rq.update_product(*product)
        # print(product)
        await rq.update_product2(product_tt_id=product[0],
                                 product_tt_code=product[1],
                                 name=product[2],
                                 purchase_price=product[3],
                                 retail_price=product[4],
                                 url=product[5])
    await message.answer(f"Завершено")
    await state.clear()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(f"Бот умеет"
                         f"\n- Искать товары по id"
                         f"\n- Искать товары по коду товара"
                         f"\n- Искать товары по ссылке\n\n"
                         f"Можно отправить файл с ссылками и в ответ бот пришлет файл с результатами парсинга")


# TODO сделать возможность очищать логи только ролям 99
@router.message(Command("clear_log"))
async def cmd_clear_log(message: Message):
    user = await rq.get_user_by_tg(message.from_user.id)
    if user.role == 99:
        with open("logs.log", 'w') as file:
            file.write('')
        logging.info('Очистка логов')
        await message.answer(f"Логи очищены")
    else:
        logging.error('Запрос на очистку логов - не прошла проверка пользователя')
        await message.answer(f"У вас нет доступа для выполнения данной команды")


@router.message(Command("backup"))
async def cmd_backup(message: Message):
    logging.info('Запрос backup_db')
    user = await rq.get_user_by_tg(message.from_user.id)
    if user.role == 99:
        await message.reply_document(
            document=FSInputFile(
                path='db.sqlite3',
                filename='backup_db.sqlite3',
            ),
        )
        logging.info('Запрос backup_db - пользователь принят')
    else:
        logging.error('Запрос backup_db - не прошла проверка пользователя')


async def add_tt_products(data: Workbook):
    default_sheet_name = "товары"
    data = tryDefaultSheetName(wb_data=data, name=default_sheet_name)

    product_list = list()
    maxCheckRow = data.max_row + 1  # поиск ссылок в строках
    for row in range(0, maxCheckRow):
        product_tt_id = data.cell(row=row + 1, column=1).value
        name = ''
        url = data.cell(row=row + 1, column=2).value
        purchase_price = data.cell(row=row + 1, column=3).value
        retail_price = data.cell(row=row + 1, column=4).value
        product_tt_code = data.cell(row=row + 1, column=6).value
        product_list.append([product_tt_id, product_tt_code, name, url, purchase_price, retail_price])
        await rq.add_tt_product2(product_tt_id=product_tt_id,
                                 product_tt_code=product_tt_code,
                                 name=name,
                                 url=url,
                                 purchase_price=purchase_price,
                                 retail_price=retail_price)


@router.message(F.content_type == ContentType.DOCUMENT)
async def get_doc(message: Message, bot: Bot):
    if message.document.file_name == 'товары ТТ.xlsx':
        file_id = message.document.file_id
        input_directory = r'input_data/'
        if not os.path.exists(input_directory):
            os.mkdir(input_directory)
        input_name = "input.xlsm"
        input_file = input_directory + input_name
        await Bot.download(bot, file_id, input_file, 120)
        input_file = openpyxl.load_workbook(input_file)
        start = time.perf_counter()
        await message.answer('Файл обрабатывается...')
        await add_tt_products(input_file)
        print(f"Выполнение заняло {time.perf_counter() - start:0.4f} секунд")
        return
    await rq.set_user(tg_id=message.from_user.id,
                      firstname=message.from_user.first_name,
                      lastname=message.from_user.last_name,
                      subscribed=0,
                      role=1)

    file_id = message.document.file_id
    input_directory = r'input_data/'
    if not os.path.exists(input_directory):
        os.mkdir(input_directory)
    input_name = "input.xlsm"
    input_file = input_directory + input_name
    await Bot.download(bot, file_id, input_file, 120)

    input_file = openpyxl.load_workbook(input_file)
    start = time.perf_counter()
    await message.answer('Файл обрабатывается...')
    wb = await Work_With_File(input_file)
    print(f"Выполнение заняло {time.perf_counter() - start:0.4f} секунд")
    output_directory = r'output_data/'
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    output_name = "output.xlsx"
    output_file = datetime.now().strftime(output_directory + output_name)
    wb.save(output_file)

    await message.reply_document(
        document=FSInputFile(
            path=output_file,
            filename=output_name,
        ),
    )


async def find_products(text):
    logging.info("Поиск по ID")
    product = await rq.get_product_by_tt_id(text.split(' ')[0])
    if product is None:
        logging.info("Поиск по коду")
        product = await rq.get_product_by_tt_code(text.split(' ')[0])
        if product is None:
            logging.info("Поиск по ссылке")
            product = await rq.get_products_by_link(text)
            if product is None:
                logging.info("Поиск по названию")
                product = await rq.get_products_by_name(text)
    return product


# @router.message(F.text.contains('товар'))
@router.message()
async def get_links(message: Message):
    products = await find_products(message.text)
    for product in products:
        logging.info("Перебор")
        if product is not None:
            await message.answer(text="Найден товар",
                                 disable_notification=True,
                                 disable_web_page_preview=True)
            data = await parsing_one(product.url)
            await message.answer(text=f"Товар: \nid: {product.product_tt_id}"
                                      f"\nКод товара: {product.product_tt_code}"
                                      f"\nНаименование: {product.name}"
                                      f"\nСсылка: {product.url}"
                                      f"\nЗакуп: {product.purchase_price}"
                                      f"\nРозница: {product.retail_price}"
                                      f"\nДата внесения: {product.update_date}"
                                      f"\n\nТекущее наименование: {data['name']}"
                                      f"\n\nТекущая РЦ: {data['price']}",
                                 disable_notification=True,
                                 disable_web_page_preview=True)
            links = list(await rq.get_links_by_tt_id(product.product_tt_id))
            if len(links) != 0:
                await message.answer(text=f"Найдено {len(links)}",
                                     disable_notification=True)
                for link in links:
                    data = await parsing_one(link.url)
                    await message.answer(text=f"Ссылка: {link.url}\n\n"
                                              f"Наименование: {data['name']}\n\n"
                                              f"Цена: {data['price']}\n",
                                         disable_notification=True,
                                         disable_web_page_preview=True)
            else:
                await message.answer(text=f"Ссылок не найдено",
                                     disable_notification=True)

        else:
            await message.answer(text="Товар не найден",
                                 disable_notification=True,
                                 disable_web_page_preview=True)
