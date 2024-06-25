import openpyxl
from aiogram import F, Bot, Router
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
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
    listOfSheets = list()
    for s in sheets:
        listOfSheets.append(s)
        print(str(listOfSheets.index(s)) + " | " + s)


def chooseSheet(wb):
    printSheets(wb.sheetnames)
    print('Введите индекс листа: ')
    sheetIndex = input()
    ws = wb.sheetnames[int(sheetIndex)]
    return ws


def tryDefaultSheetName(wbData, Name):
    try:
        return wbData[Name]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        try:
            return wbData[str(Name).lower()]
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            try:
                return wbData[str(Name).upper()]
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                sheet = chooseSheet(wbData)
    return wbData[sheet]


#inputFile - файл для парсинга
#return - Excel файл с результатами парсинга
def Work_With_File(data):
    #data = openpyxl.load_workbook(inputFile)
    defaultSheetName = "Ссылки"
    data = tryDefaultSheetName(wbData=data, Name=defaultSheetName)

    list_URL = list()
    maxCheckRow = data.max_row + 1  #поиск ссылок в строках
    maxCheckColumn = 20  #поиск ссылок в колонках
    for i in range(0, maxCheckRow):
        for j in range(0, maxCheckColumn):
            cell_obj = data.cell(row=i + 1, column=j + 1)
            if "http" in str(cell_obj.value) and "." in str(cell_obj.value):
                list_URL.append(cell_obj.value)

    wb = Workbook()
    ws = wb.active
    ws.title = "Output data"
    ws = parsing(list_URL, ws)
    return wb





# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!")


@router.message(F.content_type == ContentType.DOCUMENT)
async def get_doc(message: Message, bot: Bot):
    file_id = message.document.file_id
    print(file_id)
    path = "input_data/input.xlsx"
    await Bot.download(bot, file_id, path, 120)

    inputFile = openpyxl.load_workbook(path)
    start = time.perf_counter()
    wb = Work_With_File(inputFile)
    print(f"Выполнение заняло {time.perf_counter() - start:0.4f} секунд")
    outputDirectory = r'output_data/'
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
    print(outputDirectory)
    filename = datetime.now().strftime(outputDirectory + "output_%Y-%m-%d_%H-%M-%S.xlsx")
    wb.save(filename)
    await message.answer_document(open(filename, 'rb'))
