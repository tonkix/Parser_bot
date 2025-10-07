import logging
import app.parsing as pars


# парсинг списка ссылок
async def parsing(uniq_url_list, ws):
    logging.info('Parsing started')
    output_list = list()
    for url in uniq_url_list:
        if url is not None:
            try:
                result = await parsing_one(url)
            except Exception as err:
                mes = (f"[ERROR] {url} Unexpected {err=}, {type(err)=}\n" +
                       str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list)) + f" // [ERROR]\n"
                       f"--------------------------------------------------------------------------")
                print(mes)
                logging.error(mes)
                continue
            mes = (str(uniq_url_list.index(url) + 1) + " of " + str(len(uniq_url_list)) +
                   f" // [OK]\n"
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

        elif "autoproduct.biz" in url:
            result = await pars.autoproduct_parsing(url)
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

        elif 'xn----7sb4bdnh.xn--p1ai' in url:
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
            result = await pars.alphardaudio_parsing(url)
            price = result['price']
            name = result['name']

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
            result = await pars.autodemic_parsing(url)
            price = result['price']
            name = result['name']

        elif "original-detal.ru" in url:
            result = await pars.original_detal_parsing(url)
            price = result['price']
            name = result['name']

        elif "лада.онлайн" in url:
            result = await pars.lada_online_parsing(url)
            price = result['price']
            name = result['name']

        elif "xn--80aal0a.xn--80asehdb" in url:
            result = await pars.lada_online_parsing(url)
            price = result['price']
            name = result['name']

        elif "nvs-car.ru" in url:
            result = await pars.nvs_car_parsing(url)
            price = result['price']
            name = result['name']

        elif "car-team.ru" in url:
            result = await pars.car_team_parsing(url)
            price = result['price']
            name = result['name']

        elif "standart-detail.ru" in url:
            result = await pars.standart_detail_parsing(url)
            price = result['price']
            name = result['name']

        elif "sal-man.ru" in url:
            result = await pars.salman_parsing(url)
            price = result['price']
            name = result['name']

        elif "avtozap63.ru" in url:
            result = await pars.avtozap_parsing(url)
            price = result['price']
            name = result['name']

        elif "lada-sport.ru" in url:
            result = await pars.lada_sport_parsing(url)
            price = result['price']
            name = result['name']

        elif "komponentavto.ru" in url:
            result = await pars.komponentavto_parsing(url)
            price = result['price']
            name = result['name']

        elif "avito.ru" in url:
            result = await pars.avito_parsing(url)
            price = result['price']
            name = result['name']

        # TODO не работает, проблема с сертификатом
        elif "bi-bi.ru" in url:
            result = await pars.bibi_parsing(url)
            price = result['price']
            name = result['name']

        elif "ferrum.group" in url:
            result = await pars.ferrum_parsing(url)
            price = result['price']
            name = result['name']

        elif "ozon.ru" in url:
            result = await pars.ozon_parsing(url)
            price = result['price']
            name = result['name']

        else:
            logging.error(f"{url} - not found method")
            price = ""
            name = ""

    return {"url": url, "name": name, "price": price}
