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
        page = requests.get(url, verify=False)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find('span', id='e-curr-price').text)
        name = (bs.find('h1', class_='text_title m0 p0').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)
        '''try:
            from selenium import webdriver
            from selenium.webdriver import ChromeOptions

            options = ChromeOptions()
            options.add_argument("--headless=new")
            browser = webdriver.Chrome(options=options)
            browser.get(url)
            generated_html = browser.page_source
            browser.quit()
            bs = BeautifulSoup(generated_html, 'html.parser')

            price = priceToINT(bs.find('span', id='e-curr-price').text)
            name = (bs.find('h1', class_='text_title m0 p0').text
                    .strip())
            return {"price": price, "name": name}
        except Exception as err:
            mes = f"{url} Unexpected {err=}, {type(err)=}"
            print(mes)
            logging.error(mes)'''


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


async def aston_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('p', class_='sku__price').text
        price = priceToINT(price)
        name = (bs.find('div', class_='sku__heading').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def prestigeltd_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', class_='item-current-price').text
        price = priceToINT(price)
        name = (bs.find('span', class_='intec-cl-text-hover').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def store_starline_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', class_='price mr-3').text
        price = priceToINT(price)
        name = (bs.find('h2', itemprop="name").find('em').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def starline_russia_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = (bs.find('div',
                         class_='woocommerce-product-details__short-description').find('p').text)
        price = priceToINT(price)
        name = (bs.find('h1', class_='product_title entry-title').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def avt_tuning_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='item_price').text
        price = priceToINT(price)
        name = (bs.find('h2', '').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def gearbox63_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='autocalc-product-price').text
        price = priceToINT(price)
        name = (bs.find('h1', class_='h1-prod-name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def avtoall_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', class_="d-flex align-items-center").text
        price = priceToINT(price)
        name = (bs.find('div', class_='heading').find('span', '').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def xenon63_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='priceVal').text
        price = priceToINT(price)
        name = (bs.find('h1', class_='changeName').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def tuningprosto_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', class_='product-detail__price font-heavy').find('div').find('span').text
        price = priceToINT(price)
        name = (bs.find('h1', class_='product-detail__title font-bold').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def shop_bear_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='price_value').text
        price = priceToINT(price)
        name = (bs.find('h1', id='pagetitle').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def loudsound_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', itemprop='price').text
        price = priceToINT(price)
        name = (bs.find('h1', itemprop='name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def satox_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='num').text
        price = priceToINT(price)
        name = (bs.find('h1', itemprop='name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


async def rezkon_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', class_='price').text
        price = priceToINT(price)
        name = (bs.find('div', class_='h2').text
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
