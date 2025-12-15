import json
import logging
import requests
import undetected_chromedriver as uc
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


def priceToINT(price):
    try:
        price = "".join(filter(str.isdigit, price))
        return int(price)
    except ValueError:
        return price


# https://jsonformatter.org/
def get_ozon_json(url):
    # start = time.perf_counter()
    url = url.split('?')[0]
    json_url = f"https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fproduct%2F{url.split('product/')[1]}"

    service = ChromeService(ChromeDriverManager().install())
    driver = uc.Chrome(service=service, headless=True, use_subprocess=False, user_multi_procs=True)
    # print(f"Ссылка заняла {time.perf_counter() - start:0.4f} секунд")
    stealth(driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(json_url)
    try:
        element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.TAG_NAME, "pre"))
        )
    except TimeoutException:
        print("[ERROR] Тайм-аут")
        driver.quit()
    # print(f"Ссылка заняла {time.perf_counter() - start:0.4f} секунд")
    generated_html = driver.page_source

    driver.quit()

    bs = BeautifulSoup(generated_html, "html.parser")
    json_data = bs.find('pre').text

    return json.loads(str(json_data))


def ozon_parsing(url):
    try:
        parsed_data = get_ozon_json(url)
        # parsed_data = get_fast_ozon_json(url)
        temp_data = parsed_data['widgetStates']

        price_data = temp_data['webPrice-3121879-default-1']
        price = json.loads(str(price_data))
        try:
            price = price['cardPrice']
        except Exception as err:
            mes = f"[ERROR] {url} Unexpected {err=}, {type(err)=}"
            print(mes)
            price = price['price']
        price = priceToINT(price)

        name_data = temp_data['webStickyProducts-726428-default-1']
        name = json.loads(str(name_data))
        name = name['name']
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"[ERROR] {url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def alphardaudio_parsing(url):
    try:
        driver = uc.Chrome(headless=True, use_subprocess=False)
        stealth(driver,
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        driver.get(url)
        # driver.implicitly_wait(10)
        generated_html = driver.page_source
        driver.quit()

        bs = BeautifulSoup(generated_html, 'html.parser')
        price = bs.find('div', class_='modification_price').find('span').text
        price = priceToINT(price)
        name = (bs.find('h1', class_='h3').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def loudsound_parsing(url):
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


def motorring_parsing(url):
    try:
        urllib3.disable_warnings()
        from curl_cffi import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/141.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'cookie': 'PHPSESSID=455be602b61b30e47be0a2188c6fda1a; __ddgid_=XwSi5UyiCLtGmNNt; '
                      '__ddgmark_=QiPdyGLwJAXwReHB; __ddg2_=NlXqiRbhPF4ODIlu; __ddg1_=oaKXEHc7AsNulzdZe3ji; '
                      'page_state=[{"id":"164","page":"0","is_filter":true}]; __ddg9_=80.234.92.236; '
                      '__ddg5_=HNHXgARPfXYXoyzH; __ddg10_=1760434223; __ddg8_=kmt9syEdBxjxb9wv',
            'Connection': 'keep-alive'}

        page = requests.get(url, verify=False, impersonate="safari", headers=headers)
        bs = BeautifulSoup(page.text, "lxml")

        # новый
        # price = priceToINT(bs.find('span', class_='current__price').text)
        # name = (bs.find('h1', class_='title__head').text

        # старый
        price = priceToINT(bs.find('span', id='e-curr-price').text)
        name = (bs.find('h1', id='e-name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"[ERROR] {url} Unexpected {err=}, {type(err)=}"
        # print(bs)
        print(mes)
        logging.error(mes)


def autoproduct_parsing(url):
    try:
        urllib3.disable_warnings()
        page = requests.get(url, verify=False)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find('div', class_='product-main__right-block')
                           .find('div', class_='price').find('span').text)
        name = (bs.find('h2', class_='title').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"[ERROR] {url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def lecar_parsing(url):
    try:
        urllib3.disable_warnings()
        from curl_cffi import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/141.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'cookie': 'PHPSESSID=455be602b61b30e47be0a2188c6fda1a; __ddgid_=XwSi5UyiCLtGmNNt; '
                      '__ddgmark_=QiPdyGLwJAXwReHB; __ddg2_=NlXqiRbhPF4ODIlu; __ddg1_=oaKXEHc7AsNulzdZe3ji; '
                      'page_state=[{"id":"164","page":"0","is_filter":true}]; __ddg9_=80.234.92.236; '
                      '__ddg5_=HNHXgARPfXYXoyzH; __ddg10_=1760434223; __ddg8_=kmt9syEdBxjxb9wv',
            'Connection': 'keep-alive'}

        page = requests.get(url, verify=False, impersonate="safari", headers=headers)
        bs = BeautifulSoup(page.text, "lxml")
        # print(bs)
        price = priceToINT(bs.find('div', class_='OfferCart_price__2PerE').text)
        name = (bs.find('h1', class_='title_title__V0fDu ewddmpm3 css-1kg7k5a e1kw2ndg0').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"[ERROR] {url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def timeturbo_parsing(url):
    try:
        page = requests.get(url, verify=False)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find('span', id='price__new-val font_24').text)
        name = (bs.find('h1', class_='font_32 switcher-title js-popup-title font_20--to-600').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def sport33_parsing(url):
    try:
        urllib3.disable_warnings()
        page = requests.get(url, verify=False)
        bs = BeautifulSoup(page.text, "lxml")
        price = priceToINT(bs.find('span', class_='priceVal').text)
        name = (bs.find('h1').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def mag_demfi_parsing(url):
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


def aston_parsing(url):
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


def prestigeltd_parsing(url):
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


def store_starline_parsing(url):
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


def starline_russia_parsing(url):
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


def avt_tuning_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='item_price').text
        price = priceToINT(price)
        name = (bs.find('h2').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def gearbox63_parsing(url):
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


def avtoall_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('b', class_="c1 price-internet").text
        price = priceToINT(price)
        name = (bs.find('span', itemprop='name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def xenon63_parsing(url):
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


def tuningprosto_parsing(url):
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


def shop_bear_parsing(url):
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


def satox_parsing(url):
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


def autodemic_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', class_='js-price-hide product-price').find('span').text
        price = priceToINT(price)
        name = (bs.find('h1', class_='product-title').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def original_detal_parsing(url):
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


def lada_online_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='cart-options-cost-value').text
        price = priceToINT(price)
        name = (bs.find('div', id='dle-content').find('h1').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def car_team_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='prices-current js-prices-current').text
        price = priceToINT(price)
        name = (bs.find('h1', itemprop='name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def nvs_car_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='price large nowrap').text
        price = priceToINT(price)
        name = (bs.find('span', itemprop='name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def standart_detail_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', class_='price-number').text
        price = priceToINT(price)
        name = (bs.find('h1', itemprop='name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def avtozap_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('div', itemprop='price').find('p').text
        price = priceToINT(price)
        name = (bs.find('div', itemprop='name').find('h1').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def lada_sport_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='productprice').text
        price = priceToINT(price)
        name = (bs.find('h1', class_='producth1').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def komponentavto_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='price__new-val font_24').text
        price = priceToINT(price)
        name = (bs.find('h1', class_='font_32 switcher-title js-popup-title font_20--to-600').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def rezkon_parsing(url):
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


def salman_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        price = bs.find('span', class_='woocommerce-Price-amount amount').find('bdi').text
        price = priceToINT(price) / 100
        name = (bs.find('h1', class_='product_title entry-title').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def ferrum_parsing(url):
    try:
        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        try:

            price = bs.find('h2', class_='price discounted').text
        except Exception as err:
            price = bs.find('h2', class_='price').text
            mes = f"Unexpected {err=}, {type(err)=}"
            logging.error(mes)

        price = priceToINT(price)
        name = (bs.find('h1').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)


def avito_parsing(url):
    try:
        options = ChromeOptions()
        options.add_argument("--headless=true")

        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.implicitly_wait(5)
        driver.get(url)
        generated_html = driver.page_source
        driver.quit()

        bs = BeautifulSoup(generated_html, 'html.parser')
        price = bs.find('span', itemprop='price').text
        price = priceToINT(price)
        name = (bs.find('h1', itemprop='name').text
                .strip())
        return {"price": price, "name": name}
    except Exception as err:
        mes = f"{url} Unexpected {err=}, {type(err)=}"
        print(mes)
        logging.error(mes)
