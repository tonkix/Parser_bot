import logging
from bs4 import BeautifulSoup
import requests


def priceToINT(price):
    try:
        price = "".join(filter(str.isdigit, price))
        return int(price)
    except ValueError:
        return price


# class, itemprop, id
async def parsing(list_url, ws):
    logging.info('Parsing started')
    list_url = list(set(list_url))
    output_dict = {}
    for s in list_url:
        if s is not None:
            try:
                page = requests.get(s)
                bs = BeautifulSoup(page.text, "lxml")

                if "motorring.ru" in s:
                    price = bs.find('span', id='e-curr-price').text
                    price = priceToINT(price)
                    name = bs.find('h1', class_='text_title m0 p0').text

                elif 'timeturbo.ru' in s:
                    price = bs.find('span', class_='price__new-val font_24').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='font_32 switcher-title js-popup-title font_20--to-600').text
                            .strip())

                elif "33sport.ru" in s:
                    price = bs.find('span', class_='priceVal').text
                    price = priceToINT(price)
                    name = bs.find('h1', '').text

                elif "mag.demfi.ru" in s:
                    price = (bs.find('div', itemprop='price').contents[0])
                    price = priceToINT(price)
                    name = (bs.find('div', class_="product-box").find('h1').text
                            .strip())

                elif 'ас-тон.рф' in s:
                    price = bs.find('p', class_='sku__price').text
                    price = priceToINT(price)
                    name = (bs.find('div', class_='sku__heading').text
                            .strip())

                elif 'prestigeltd.ru' in s:
                    price = bs.find('div', class_='item-current-price').text
                    price = priceToINT(price)
                    name = (bs.find('span', class_='intec-cl-text-hover').text
                            .strip())

                elif 'store.starline.ru' in s:
                    price = bs.find('div', class_='price mr-3').text
                    price = priceToINT(price)
                    name = (bs.find('h2', itemprop="name").find('em').text
                            .strip())

                elif 'starline-russia' in s:
                    price = (bs.find('div',
                                     class_='woocommerce-product-details__short-description').find('p').text)
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='product_title entry-title').text
                            .strip())

                elif "avttuning.ru" in s:
                    price = bs.find('span', class_='item_price').text
                    price = priceToINT(price)
                    name = (bs.find('h2', '').text
                            .strip())

                elif "gearbox63" in s:
                    price = bs.find('span', class_='autocalc-product-price').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='h1-prod-name').text
                            .strip())

                elif "avtoall.ru" in s:
                    price = bs.find('div', class_="d-flex align-items-center").text
                    price = priceToINT(price)
                    name = (bs.find('div', class_='heading').find('span', '').text
                            .strip())

                elif "xenon63" in s:
                    price = bs.find('span', class_='priceVal').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='changeName').text
                            .strip())

                elif "tuningprosto" in s:
                    price = bs.find('span', id='bx_117848907_10953_price').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='product-detail__title font-bold').text
                            .strip())

                elif "alphardaudio.ru" in s:
                    from selenium import webdriver
                    from selenium.webdriver import ChromeOptions

                    options = ChromeOptions()
                    options.add_argument("--headless=new")
                    browser = webdriver.Chrome(options=options)
                    browser.get(s)
                    generated_html = browser.page_source
                    browser.quit()
                    bs = BeautifulSoup(generated_html, 'html.parser')
                    price = bs.find('div', class_='modification_price').find('span').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='h3').text
                            .strip())

                elif "shop-bear.ru" in s:
                    price = bs.find('span', class_='price_value').text
                    price = priceToINT(price)
                    name = (bs.find('h1', id='pagetitle').text
                            .strip())

                elif "loudsound.ru" in s:
                    price = bs.find('span', itemprop='price').text
                    price = priceToINT(price)
                    name = (bs.find('h1', itemprop='name').text
                            .strip())

                elif "satox.ru" in s:
                    price = bs.find('span', class_='num').text
                    price = priceToINT(price)
                    name = (bs.find('h1', itemprop='name').text
                            .strip())

                elif "rezkon.ru" in s:
                    price = bs.find('div', class_='price').text
                    price = priceToINT(price)
                    name = (bs.find('div', class_='h2').text
                            .strip())

                # TODO не работает
                elif "ozon.ru" in s:
                    from selenium import webdriver
                    from selenium.webdriver import ChromeOptions

                    options = ChromeOptions()
                    options.add_argument("--headless=new")
                    browser = webdriver.Chrome(options=options)
                    browser.get(s)
                    generated_html = browser.page_source
                    browser.quit()
                    bs = BeautifulSoup(generated_html, 'html.parser')
                    price = bs.find('span', class_='zl0_27 l9y_27').text
                    price = priceToINT(price)
                    name = (bs.find('h1', class_='mm3_27 tsHeadline550Medium').text
                            .strip())

                else:
                    logging.error(f"{s} - not found method")
                    price = ""
                    name = ""

            except Exception as err:
                price = ""
                name = ""
                print(str(list_url.index(s) + 1) + " of " + str(len(list_url))
                      + f"Unexpected {err=}, {type(err)=}")
                logging.error(f"{s} - {str(list_url.index(s) + 1)} of {str(len(list_url))} "
                              f"##error - Unexpected {err=}, {type(err)=}")
                continue
            print(str(list_url.index(s) + 1) + " of " + str(len(list_url)))
            logging.info(str(list_url.index(s) + 1) + " of " + str(len(list_url)))
            output_dict[s] = [name, price]
            ws.append({1: s, 2: name, 3: price})
    return output_dict
