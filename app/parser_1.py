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

                # запись уникальной ссылки с ценой выходной лист
                output_list.append([data['url'], data['name'], data['price']])
                # запись уникальной ссылки с ценой в Excel
                ws.append({1: data['url'], 2: data['name'], 3: data['price']})
                # print(data)
            except Exception as err:
                data = str(type(err))
                # print(f"\n[ERROR] Unexpected {err=}, {type(err)=}")
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

        elif 'timeturbo.ru' in url:
            result = pars.timeturbo_parsing(url)
            price = result['price']
            name = result['name']

        elif "33sport.ru" in url:
            result = pars.sport33_parsing(url)
            price = result['price']
            name = result['name']

        elif "autoproduct.biz" in url:
            result = pars.autoproduct_parsing(url)
            price = result['price']
            name = result['name']

        elif "lecar.ru" in url:
            result = pars.lecar_parsing(url)
            price = result['price']
            name = result['name']

        elif "mag.demfi.ru" in url:
            result = pars.mag_demfi_parsing(url)
            price = result['price']
            name = result['name']

        elif 'ас-тон.рф' in url:
            result = pars.aston_parsing(url)
            price = result['price']
            name = result['name']

        elif 'xn----7sb4bdnh.xn--p1ai' in url:
            result = pars.aston_parsing(url)
            price = result['price']
            name = result['name']

        elif 'prestigeltd.ru' in url:
            result = pars.prestigeltd_parsing(url)
            price = result['price']
            name = result['name']

        elif 'store.starline.ru' in url:
            result = pars.store_starline_parsing(url)
            price = result['price']
            name = result['name']

        elif 'starline-russia' in url:
            result = pars.starline_russia_parsing(url)
            price = result['price']
            name = result['name']

        elif "avttuning.ru" in url:
            result = pars.avt_tuning_parsing(url)
            price = result['price']
            name = result['name']

        elif "gearbox63" in url:
            result = pars.gearbox63_parsing(url)
            price = result['price']
            name = result['name']

        elif "avtoall.ru" in url:
            result = pars.avtoall_parsing(url)
            price = result['price']
            name = result['name']

        elif "xenon63" in url:
            result = pars.xenon63_parsing(url)
            price = result['price']
            name = result['name']

        elif "tuningprosto" in url:
            result = pars.tuningprosto_parsing(url)
            price = result['price']
            name = result['name']

        elif "alphardaudio.ru" in url:
            result = pars.alphardaudio_parsing(url)
            price = result['price']
            name = result['name']

        elif "shop-bear.ru" in url:
            result = pars.shop_bear_parsing(url)
            price = result['price']
            name = result['name']

        elif "loudsound.ru" in url:
            result = pars.loudsound_parsing(url)
            price = result['price']
            name = result['name']

        elif "satox.ru" in url:
            result = pars.satox_parsing(url)
            price = result['price']
            name = result['name']

        elif "rezkon.ru" in url:
            result = pars.rezkon_parsing(url)
            price = result['price']
            name = result['name']

        elif "autodemic.ru" in url:
            result = pars.autodemic_parsing(url)
            price = result['price']
            name = result['name']

        elif "original-detal.ru" in url:
            result = pars.original_detal_parsing(url)
            price = result['price']
            name = result['name']

        elif "лада.онлайн" in url:
            result = pars.lada_online_parsing(url)
            price = result['price']
            name = result['name']

        elif "xn--80aal0a.xn--80asehdb" in url:
            result = pars.lada_online_parsing(url)
            price = result['price']
            name = result['name']

        elif "nvs-car.ru" in url:
            result = pars.nvs_car_parsing(url)
            price = result['price']
            name = result['name']

        elif "car-team.ru" in url:
            result = pars.car_team_parsing(url)
            price = result['price']
            name = result['name']

        elif "standart-detail.ru" in url:
            result = pars.standart_detail_parsing(url)
            price = result['price']
            name = result['name']

        elif "sal-man.ru" in url:
            result = pars.salman_parsing(url)
            price = result['price']
            name = result['name']

        elif "avtozap63.ru" in url:
            result = pars.avtozap_parsing(url)
            price = result['price']
            name = result['name']

        elif "lada-sport.ru" in url:
            result = pars.lada_sport_parsing(url)
            price = result['price']
            name = result['name']

        elif "komponentavto.ru" in url:
            result = pars.komponentavto_parsing(url)
            price = result['price']
            name = result['name']

        elif "avito.ru" in url:
            result = pars.avito_parsing(url)
            price = result['price']
            name = result['name']

        elif "ferrum.group" in url:
            result = pars.ferrum_parsing(url)
            price = result['price']
            name = result['name']

        else:
            logging.error(f"{url} - not found method")
            price = ""
            name = ""

    return {"url": url, "name": name, "price": price}
