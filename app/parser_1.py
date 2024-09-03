import json
import logging
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import seleniumbase as sb
from selenium_stealth import stealth

from app.parsing import priceToINT
from app.parsing import get_ozon_json
import app.parsing as pars


# class, itemprop, id
async def parsing(uniq_url_list, ws):
    logging.info('Parsing started')
    output_list = list()
    for url in uniq_url_list:
        if url is not None:
            try:
                result = await parsing_one(url)
            except Exception as err:
                mes = (str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list))
                       + f" {url} Unexpected {err=}, {type(err)=}")
                print(mes)
                logging.error(mes)
                continue
            mes = str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list))
            print(mes)
            logging.info(mes)

            # запись уникальной ссылки с ценой выходной лист
            output_list.append([result['url'], result['name'], result['price']])

            # запись уникальной ссылки с ценой в Эксель
            ws.append({1: result['url'], 2: result['name'], 3: result['price']})
    return output_list


async def parsing_one(url):
    logging.info('Parsing started')
    price = ''
    name = ''
    if url is not None:

        if "motorring.ru" in url:
            result = await pars.motorring_parsing(url)
            price = result['price']
            name = result['name']

        elif 'timeturbo.ru' in url:
            result = await pars.timeturbo_parsing(url)
            price = result['price']
            name = result['name']

        elif "33sport.ru" in url:
            result = await pars.sport33_parsing(url)
            price = result['price']
            name = result['name']

        elif "mag.demfi.ru" in url:
            result = await pars.mag_demfi_parsing(url)
            price = result['price']
            name = result['name']

        elif 'ас-тон.рф' in url:
            result = await pars.aston_parsing(url)
            price = result['price']
            name = result['name']

        elif 'prestigeltd.ru' in url:
            result = await pars.prestigeltd_parsing(url)
            price = result['price']
            name = result['name']

        elif 'store.starline.ru' in url:
            result = await pars.store_starline_parsing(url)
            price = result['price']
            name = result['name']

        elif 'starline-russia' in url:
            result = await pars.starline_russia_parsing(url)
            price = result['price']
            name = result['name']

        elif "avttuning.ru" in url:
            result = await pars.avt_tuning_parsing(url)
            price = result['price']
            name = result['name']

        elif "gearbox63" in url:
            result = await pars.gearbox63_parsing(url)
            price = result['price']
            name = result['name']

        elif "avtoall.ru" in url:
            result = await pars.avtoall_parsing(url)
            price = result['price']
            name = result['name']

        elif "xenon63" in url:
            result = await pars.xenon63_parsing(url)
            price = result['price']
            name = result['name']

        elif "tuningprosto" in url:
            result = await pars.tuningprosto_parsing(url)
            price = result['price']
            name = result['name']

        elif "alphardaudio.ru" in url:
            from selenium import webdriver
            from selenium.webdriver import ChromeOptions

            options = ChromeOptions()
            options.add_argument("--headless=new")
            browser = webdriver.Chrome(options=options)
            browser.get(url)
            generated_html = browser.page_source
            browser.quit()
            bs = BeautifulSoup(generated_html, 'html.parser')
            price = bs.find('div', class_='modification_price').find('span').text
            price = priceToINT(price)
            name = (bs.find('h1', class_='h3').text
                    .strip())

        elif "shop-bear.ru" in url:
            result = await pars.shop_bear_parsing(url)
            price = result['price']
            name = result['name']

        elif "loudsound.ru" in url:
            result = await pars.loudsound_parsing(url)
            price = result['price']
            name = result['name']

        elif "satox.ru" in url:
            result = await pars.satox_parsing(url)
            price = result['price']
            name = result['name']

        elif "rezkon.ru" in url:
            result = await pars.rezkon_parsing(url)
            price = result['price']
            name = result['name']

        elif "autodemic.ru" in url:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            price = bs.find('div', class_='js-price-hide product-price').find('span').text
            price = priceToINT(price)
            name = (bs.find('h1', class_='product-title').text
                    .strip())

        elif "original-detal.ru" in url:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            price = bs.find('span', class_='price_value').text
            price = priceToINT(price)
            name = (bs.find('h1', id='pagetitle').text
                    .strip())

        elif "лада.онлайн" in url:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            price = bs.find('span', class_='cart-options-cost-value').text
            price = priceToINT(price)
            name = (bs.find('div', id='dle-content').find('h1').text
                    .strip())

        elif "xn--80aal0a.xn--80asehdb" in url:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            price = bs.find('span', class_='cart-options-cost-value').text
            price = priceToINT(price)
            name = (bs.find('div', id='dle-content').find('h1').text
                    .strip())

        elif "standart-detail.ru" in url:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            price = bs.find('div', class_='price-number').text
            price = priceToINT(price)
            name = (bs.find('h1', itemprop='name').text
                    .strip())

        elif "sal-man.ru" in url:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            price = bs.find('span', class_='woocommerce-Price-amount amount').find('bdi').text
            price = priceToINT(price) / 100
            name = (bs.find('h1', class_='product_title entry-title').text
                    .strip())

        # TODO не работает, проблема с сертификатом
        elif "bi-bi.ru" in url:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            price = bs.find('span', class_='price card-price__cur').text
            price = priceToINT(price)
            name = (bs.find('h1', class_='section__hl').text
                    .strip())

        elif "ferrum.group" in url:
            try:
                page = requests.get(url)
                bs = BeautifulSoup(page.text, "lxml")

                price = bs.find('h2', class_='price discounted').text
            except Exception as err:
                price = bs.find('h2', class_='price').text
                mes = f"Unexpected {err=}, {type(err)=}"
                logging.error(mes)

            price = priceToINT(price)
            name = (bs.find('h1').text
                    .strip())

        elif "ozon.ru" in url:
            parsed_data = get_ozon_json(url)
            temp_data = parsed_data['widgetStates']

            price_data = temp_data['webPrice-3121879-default-1']
            price = json.loads(str(price_data))
            try:
                price = price['cardPrice']
            except Exception as err:
                mes = f" {url} Unexpected {err=}, {type(err)=}"
                print(mes)
                price = price['price']
            price = priceToINT(price)

            name_data = temp_data['webStickyProducts-726428-default-1']
            name = json.loads(str(name_data))
            name = name['name']

        else:
            logging.error(f"{url} - not found method")
            price = ""
            name = ""

    return {"url": url, "name": name, "price": price}
