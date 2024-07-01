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
from app.parser_1 import parsing

router = Router()
load_dotenv()


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


def find_elem_by_url(url, parsing_result):
    for e in parsing_result:
        if url == e[0]:
            return e


# inputFile - файл для парсинга
# return - Excel файл с результатами парсинга
# TODO дописать чтобы из файла брало id товара
async def Work_With_File(data):
    # data = openpyxl.load_workbook(inputFile)
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
            data = find_elem_by_url(k[1], parsing_result)
            print(str(k[0]) + "/" + str(k[1]))
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

    '''for key in id_url_dict:
        ws.append({1: key,
                   2: id_url_dict[key],
                   3: name_price_dict[id_url_dict[key]][0],
                   4: name_price_dict[id_url_dict[key]][1]})
        print(str(key) + "/" + id_url_dict[key])
        await rq.add_link(product_id=key,
                          url=id_url_dict[key],
                          name=name_price_dict[id_url_dict[key]][0],
                          price=name_price_dict[id_url_dict[key]][1])'''
    return wb


@router.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(tg_id=message.from_user.id,
                      firstname=message.from_user.first_name,
                      lastname=message.from_user.last_name,
                      subscribed=0,
                      role=1)
    await message.answer("Hello!")


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


async def add_tt_products(data):
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
        await rq.add_tt_product(product_tt_id=product_tt_id,
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


@router.message(F.text.contains('товар'))
async def get_links(message: Message):
    product = await rq.get_product_by_tt_id(message.text.split(' ')[1])
    links = list(await rq.get_links_by_tt_id(message.text.split(' ')[1]))
    await message.answer(text=f"Товар: \nid: {product.product_tt_id}"
                              f"\nКод товара: {product.product_tt_code}"
                              f"\nНаименование: {product.name}"
                              f"\nСсылка: {product.url}"
                              f"\nЗакуп: {product.purchase_price}"
                              f"\nРозница: {product.retail_price}"
                              f"\nДата внесения: {product.update_date}",
                         disable_notification=True)
    await message.answer(text=f"Найдено {len(links)} ссылок",
                         disable_notification=True)
    for link in links:
        await message.answer(text=link.url,
                             disable_notification=True,
                             disable_web_page_preview=True)


@router.message()
async def any_reply(message: Message):
    await rq.set_user(tg_id=message.from_user.id,
                      firstname=message.from_user.first_name,
                      lastname=message.from_user.last_name,
                      subscribed=0,
                      role=1)
    await message.reply('У меня нет инструкции на такое сообщение')
