import json
import logging
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import seleniumbase as sb
from selenium_stealth import stealth


# https://jsonformatter.org/
def get_ozon_json(url):
    json_url = url.split('product/')[1]
    json_url = f"https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fproduct%2F{json_url}"
    # print(json_url)
    driver = sb.Driver(browser='chrome', headless=True, uc=True)
    stealth(driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            wait=webdriver.Chrome.implicitly_wait(driver, 100.00))

    driver.get(json_url)
    generated_html = driver.page_source
    bs = BeautifulSoup(generated_html, "html.parser")
    json_data = bs.find('pre').text
    driver.quit()
    return json.loads(str(json_data))


def priceToINT(price):
    try:
        price = "".join(filter(str.isdigit, price))
        return int(price)
    except ValueError:
        return price


async def motorring_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find('span', id='e-curr-price').text)
        name = (bs.find('h1', class_='text_title m0 p0').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def timeturbo_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find('span', id='price__new-val font_24').text)
        name = (bs.find('h1', class_='font_32 switcher-title js-popup-title font_20--to-600').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def sport33_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find('span', class_='priceVal').text)
        name = (bs.find('h1', '').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def mag_demfi_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = (bs.find('div', itemprop='price').contents[0])
        price = priceToINT(price)
        name = (bs.find('div', class_="product-box").find('h1').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def general_parsing(url, name_p, attr_p, name_n, attr_n):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find(name_p, id=attr_p).text)
        name = (bs.find(name_n,  class_=attr_n).text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)
