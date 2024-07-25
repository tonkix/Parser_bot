import json
import logging
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import seleniumbase as sb
from selenium_stealth import stealth


def priceToINT(price):
    try:
        price = "".join(filter(str.isdigit, price))
        return int(price)
    except ValueError:
        return price


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


# class, itemprop, id
async def parsing(uniq_url_list, ws):
    logging.info('Parsing started')
    output_list = list()
    for url in uniq_url_list:
        if url is not None:
            try:
                page = requests.get(url)
                bs = BeautifulSoup(page.text, "lxml")

                if "motorring.ru" in url:
                    price = bs.find('span', id='e-curr-price').text
                    price = priceToINT(price)
                    name = bs.find('h1', class_='text_title m0 p0').text

                elif 'timeturbo.ru' in url:
                    price = bs.find('span', class_='price__new-val font_24').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='font_32 switcher-title js-popup-title font_20--to-600').text
                            .strip())

                elif "33sport.ru" in url:
                    price = bs.find('span', class_='priceVal').text
                    price = priceToINT(price)
                    name = bs.find('h1', '').text

                elif "mag.demfi.ru" in url:
                    price = (bs.find('div', itemprop='price').contents[0])
                    price = priceToINT(price)
                    name = (bs.find('div', class_="product-box").find('h1').text
                            .strip())

                elif 'ас-тон.рф' in url:
                    price = bs.find('p', class_='sku__price').text
                    price = priceToINT(price)
                    name = (bs.find('div', class_='sku__heading').text
                            .strip())

                elif 'prestigeltd.ru' in url:
                    price = bs.find('div', class_='item-current-price').text
                    price = priceToINT(price)
                    name = (bs.find('span', class_='intec-cl-text-hover').text
                            .strip())

                elif 'store.starline.ru' in url:
                    price = bs.find('div', class_='price mr-3').text
                    price = priceToINT(price)
                    name = (bs.find('h2', itemprop="name").find('em').text
                            .strip())

                elif 'starline-russia' in url:
                    price = (bs.find('div',
                                     class_='woocommerce-product-details__short-description').find('p').text)
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='product_title entry-title').text
                            .strip())

                elif "avttuning.ru" in url:
                    price = bs.find('span', class_='item_price').text
                    price = priceToINT(price)
                    name = (bs.find('h2', '').text
                            .strip())

                elif "gearbox63" in url:
                    price = bs.find('span', class_='autocalc-product-price').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='h1-prod-name').text
                            .strip())

                elif "avtoall.ru" in url:
                    price = bs.find('div', class_="d-flex align-items-center").text
                    price = priceToINT(price)
                    name = (bs.find('div', class_='heading').find('span', '').text
                            .strip())

                elif "xenon63" in url:
                    price = bs.find('span', class_='priceVal').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='changeName').text
                            .strip())

                elif "tuningprosto" in url:
                    price = bs.find('div', class_='product-detail__price font-heavy').find('div').find('span').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='product-detail__title font-bold').text
                            .strip())

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
                    price = bs.find('span', class_='price_value').text
                    price = priceToINT(price)
                    name = (bs.find('h1', id='pagetitle').text
                            .strip())

                elif "loudsound.ru" in url:
                    price = bs.find('span', itemprop='price').text
                    price = priceToINT(price)
                    name = (bs.find('h1', itemprop='name').text
                            .strip())

                elif "satox.ru" in url:
                    price = bs.find('span', class_='num').text
                    price = priceToINT(price)
                    name = (bs.find('h1', itemprop='name').text
                            .strip())

                elif "rezkon.ru" in url:
                    price = bs.find('div', class_='price').text
                    price = priceToINT(price)
                    name = (bs.find('div', class_='h2').text
                            .strip())

                elif "autodemic.ru" in url:
                    price = bs.find('div', class_='js-price-hide product-price').find('span').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='product-title').text
                            .strip())

                elif "original-detal.ru" in url:
                    price = bs.find('span', class_='price_value').text
                    price = priceToINT(price)
                    name = (bs.find('h1', id='pagetitle').text
                            .strip())

                elif "лада.онлайн" in url:
                    price = bs.find('span', class_='cart-options-cost-value').text
                    price = priceToINT(price)
                    name = (bs.find('div', id='dle-content').find('h1').text
                            .strip())

                elif "xn--80aal0a.xn--80asehdb" in url:
                    price = bs.find('span', class_='cart-options-cost-value').text
                    price = priceToINT(price)
                    name = (bs.find('div', id='dle-content').find('h1').text
                            .strip())

                elif "standart-detail.ru" in url:
                    price = bs.find('div', class_='price-number').text
                    price = priceToINT(price)
                    name = (bs.find('h1', itemprop='name').text
                            .strip())

                # TODO не работает, проблема с сертификатом
                elif "bi-bi.ru" in url:
                    price = bs.find('span', class_='price card-price__cur').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='section__hl').text
                            .strip())

                elif "ferrum.group" in url:
                    try:
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
                    price = price['cardPrice']
                    price = priceToINT(price)

                    name_data = temp_data['webStickyProducts-726428-default-1']
                    name = json.loads(str(name_data))
                    name = name['name']

                else:
                    logging.error(f"{url} - not found method")
                    price = ""
                    name = ""

            except Exception as err:
                mes = (str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list))
                       + f" {url} Unexpected {err=}, {type(err)=}")
                print(mes)
                logging.error(mes)
                continue
            mes = str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list))
            print(mes)
            logging.info(mes)

            output_list.append([url, name, price])  # запись уникальной ссылки с ценой выходной лист
            ws.append({1: url, 2: name, 3: price})  # запись уникальной ссылки с ценой в Эксель
    return output_list


async def parsing_one(url):
    logging.info('Parsing started')
    price = ''
    name = ''
    if url is not None:
        try:
            page = requests.get(url)
            bs = BeautifulSoup(page.text, "lxml")

            if "motorring.ru" in url:
                price = bs.find('span', id='e-curr-price').text
                price = priceToINT(price)
                name = bs.find('h1', class_='text_title m0 p0').text

            elif 'timeturbo.ru' in url:
                price = bs.find('span', class_='price__new-val font_24').text
                price = priceToINT(price)
                name = (bs.find('h1', class_='font_32 switcher-title js-popup-title font_20--to-600').text
                        .strip())

            elif "33sport.ru" in url:
                price = bs.find('span', class_='priceVal').text
                price = priceToINT(price)
                name = bs.find('h1', '').text

            elif "mag.demfi.ru" in url:
                price = (bs.find('div', itemprop='price').contents[0])
                price = priceToINT(price)
                name = (bs.find('div', class_="product-box").find('h1').text
                        .strip())

            elif 'ас-тон.рф' in url:
                price = bs.find('p', class_='sku__price').text
                price = priceToINT(price)
                name = (bs.find('div', class_='sku__heading').text
                        .strip())

            elif 'prestigeltd.ru' in url:
                price = bs.find('div', class_='item-current-price').text
                price = priceToINT(price)
                name = (bs.find('span', class_='intec-cl-text-hover').text
                        .strip())

            elif 'store.starline.ru' in url:
                price = bs.find('div', class_='price mr-3').text
                price = priceToINT(price)
                name = (bs.find('h2', itemprop="name").find('em').text
                        .strip())

            elif 'starline-russia' in url:
                price = (bs.find('div',
                                 class_='woocommerce-product-details__short-description').find('p').text)
                price = priceToINT(price)
                name = (bs.find('h1', class_='product_title entry-title').text
                        .strip())

            elif "avttuning.ru" in url:
                price = bs.find('span', class_='item_price').text
                price = priceToINT(price)
                name = (bs.find('h2', '').text
                        .strip())

            elif "gearbox63" in url:
                price = bs.find('span', class_='autocalc-product-price').text
                price = priceToINT(price)
                name = (bs.find('h1', class_='h1-prod-name').text
                        .strip())

            elif "avtoall.ru" in url:
                price = bs.find('div', class_="d-flex align-items-center").text
                price = priceToINT(price)
                name = (bs.find('div', class_='heading').find('span', '').text
                        .strip())

            elif "xenon63" in url:
                price = bs.find('span', class_='priceVal').text
                price = priceToINT(price)
                name = (bs.find('h1', class_='changeName').text
                        .strip())

            elif "tuningprosto" in url:
                price = bs.find('span', id='bx_117848907_10953_price').text
                price = priceToINT(price)
                name = (bs.find('h1', class_='product-detail__title font-bold').text
                        .strip())

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
                price = bs.find('span', class_='price_value').text
                price = priceToINT(price)
                name = (bs.find('h1', id='pagetitle').text
                        .strip())

            elif "loudsound.ru" in url:
                price = bs.find('span', itemprop='price').text
                price = priceToINT(price)
                name = (bs.find('h1', itemprop='name').text
                        .strip())

            elif "satox.ru" in url:
                price = bs.find('span', class_='num').text
                price = priceToINT(price)
                name = (bs.find('h1', itemprop='name').text
                        .strip())

            elif "rezkon.ru" in url:
                price = bs.find('div', class_='price').text
                price = priceToINT(price)
                name = (bs.find('div', class_='h2').text
                        .strip())

            elif "ferrum.group" in url:
                try:
                    price = bs.find('h2', class_='price discounted').text
                except Exception as err:
                    price = bs.find('h2', class_='price').text
                    mes = f"Unexpected {err=}, {type(err)=}"
                    logging.error(mes)

                price = priceToINT(price)
                name = (bs.find('h1').text
                        .strip())

            else:
                logging.error(f"{url} - not found method")
                price = ""
                name = ""

        except Exception as err:
            mes = f"Unexpected {err=}, {type(err)=}"
            print(mes)
            logging.error(mes)
    return {"url": url, "name": name, "price": price}
