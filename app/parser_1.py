import logging
import app.parsing as pars


# парсинг списка ссылок
async def parsing(uniq_url_list, ws):
    logging.info('Parsing started')
    output_list = list()

    CONNECTIONS = 5
    import concurrent.futures
    from tqdm import tqdm

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(parsing_one, url) for url in uniq_url_list)
        for future in tqdm(concurrent.futures.as_completed(future_to_url), total=len(uniq_url_list)):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                # запись уникальной ссылки с ценой выходной лист
                output_list.append([data['url'], data['name'], data['price']])

                # запись уникальной ссылки с ценой в Эксель
                ws.append({1: data['url'], 2: data['name'], 3: data['price']})
                # print(data)

    return output_list


# парсинг одной ссылки
def parsing_one(url):
    logging.info('Parsing started')
    price = ''
    name = ''
    if url is not None:

        if "motorring.ru" in url:
            result = pars.motorring_parsing(url)
            price = result['price']
            name = result['name']

        elif "ozon.ru" in url:
            result = pars.ozon_parsing(url)
            price = result['price']
            name = result['name']

        else:
            logging.error(f"{url} - not found method")
            price = ""
            name = ""

    return {"url": url, "name": name, "price": price}


"""async def parsing(uniq_url_list, ws):
    logging.info('Parsing started')
    output_list = list()
    for url in uniq_url_list:
        if url is not None:
            try:
                result = await parsing_one(url)
            except Exception as err:
                mes = (f"[ERROR] {url} Unexpected {err=}, {type(err)=}\n" +
                       f"[ERROR] " + str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list)) + f"\n"
                       f"--------------------------------------------------------------------------")
                print(mes)
                logging.error(mes)
                continue
            mes = (f"[OK] " + str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list)) +
                   f"\n"
                   f"--------------------------------------------------------------------------")
            print(mes)
            logging.info(mes)

            # запись уникальной ссылки с ценой выходной лист
            output_list.append([result['url'], result['name'], result['price']])

            # запись уникальной ссылки с ценой в Эксель
            ws.append({1: result['url'], 2: result['name'], 3: result['price']})
    return output_list


# парсинг одной ссылки
async def parsing_one(url):
    logging.info('Parsing started')
    price = ''
    name = ''
    if url is not None:

        if "motorring.ru" in url:
            result = pars.motorring_parsing(url)
            price = result['price']
            name = result['name']

        elif "ozon.ru" in url:
            result = pars.ozon_parsing(url)
            price = result['price']
            name = result['name']

        else:
            logging.error(f"{url} - not found method")
            price = ""
            name = ""

    return {"url": url, "name": name, "price": price}"""


# парсинг одной ссылки
def parsing_one(url):
    logging.info('Parsing started')
    price = ''
    name = ''
    if url is not None:

        if "motorring.ru" in url:
            result = pars.motorring_parsing(url)
            price = result['price']
            name = result['name']

        elif "ozon.ru" in url:
            result = pars.ozon_parsing(url)
            price = result['price']
            name = result['name']

        else:
            logging.error(f"{url} - not found method")
            price = ""
            name = ""

    return {"url": url, "name": name, "price": price}
