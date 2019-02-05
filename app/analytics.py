from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import json
import time as time
import random
import re as re

def getDataFrame(num_pages):

    #num_pages = input('Quantas páginas desejas buscar históricos de celulares?')
    num_cell = 0
    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

    ids = []
    images = []
    titles = []
    last_prices = []
    current_prices = []
    payment_formats = []
    cupons_codes = []
    cupons_titles = []
    stores = []
    actives = []
    ratings = []
    likes = []

    for page in range(1, int(num_pages)+1):
        try:
            print('Acessando página: ' + str(page))
            url = 'https://www.ofertaesperta.com/categoria/celulares-e-smartphones?page=' + str(page)
            response = get(url, headers=headers)
            html_soup = BeautifulSoup(response.text, 'html.parser')

            phones_containers = html_soup.find_all('div', class_="cards")
            phones_cards = phones_containers[0].find_all('div', class_="card-col")

            for phones in phones_cards:
                try:
                    id = phones.find_all('div')[0].get('id').replace('card-', '')
                    num_cell += 1
                    print('Gerando para o ID: ' + str(id))

                    #Busca os valores pela requisição da API do ofertaesperta
                    response_json = get_all_info_by_api(id)

                    if 'cupon' in response_json:
                        cupom_obj = response_json["cupon"]
                    else:
                        cupom_obj = {'code': '-', "title": '-'}

                    #Obj para pegar as informacoes da loja
                    store_obj = response_json["store"]

                    #Appends
                    ids.append(id)
                    images.append(response_json["image_link"])
                    titles.append(response_json["title"])
                    last_prices.append(response_json["previous_price"])
                    current_prices.append(response_json["price"])
                    payment_formats.append(response_json["payment_format_primary"])
                    cupons_codes.append(cupom_obj["code"])
                    cupons_titles.append(cupom_obj["title"])
                    stores.append(store_obj["name"])
                    actives.append(response_json["active"])
                    ratings.append(response_json["rating"])
                    likes.append(response_json["likes_count"])
                except Exception:
                    print('Houve um erro na busca do celular, seguindo para o próximo...')
                    continue
            time.sleep(random.randint(1, 2))
        except Exception:
            print('Houve um erro na requisição, seguindo para a próxima página...')
            continue

    phones_df = pd.DataFrame({
        'id': ids,
        'phone_title': titles,
        'last_price': last_prices,
        'current_price': current_prices,
        'payment_format': payment_formats,
        'cupom_code': cupons_codes,
        'cupom_title': cupons_titles,
        'store': stores,
        'active': actives,
        'rating': ratings,
        'likes_count': likes
    })

    print('Data Frame criado para um total de {} celulares...'.format(num_cell))

    return phones_df

def get_all_info_by_api(id):
    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    url = 'https://www.ofertaesperta.com/api/offers/' + str(id)
    response = get(url, headers=headers)
    response_json = json.loads(response.text)

    return response_json

def df_to_csv(data_frame, fileName):
    try:
        data_frame.to_csv(fileName, sep='\t', encoding='utf-8')
        print('Data Frame salvo com sucesso para phones.csv')
        return True
    except Exception as E:
        print('Houve um erro ao salvar o Data Frame para phones.csv: ' + E)
        return False


def csv_to_df(file_name):
    phones_df = pd.read_csv(file_name, sep='\t', encoding='utf-8')
    print('Data Frame gerado com sucesso a partir do csv {}'.format(file_name))
    return phones_df

def append_memories(phones_df):
    memories = []
    for h in phones_df.phone_title:
        # Expressao regular para pegar somente numeros antes de GB, de até 3 digitos
        n = [s for s in re.findall(r"(\d{2,3}GB)", h)]
        memories.append(n)

    memoriesT = pd.DataFrame(memories)[0]
    phones_df['Ram'] = memoriesT

    return phones_df

def clear_data(phones_df):

    #Limpo as linhas onde não foi possível buscar o total de memória Ram ou o preço vazio
    phones_df.dropna(subset=['Ram', 'last_price'], inplace=True)
    phones_df.reset_index(inplace=True, drop=True)

    #Current_price
    y = []
    for x in phones_df.current_price:
        if y:
            y.append(float(x.replace('.', '').replace(',', '.')))
        else:
            y.append('ERROR')

    phones_df['current_price'] = y

    #Last_price
    y = []
    for x in phones_df.last_price:
        if x:
            y.append(float(x.replace('.', '').replace(',', '.')))
        else:
            y.append('ERROR')

    phones_df['last_price'] = y

    #Limpo as linhas onde não possuem o preço antigo ou preço atual
    phones_df = phones_df[phones_df['current_price'] != 'ERROR']
    phones_df = phones_df[phones_df['last_price'] != 'ERROR']

    return phones_df

def new_info(phones_df):

    #Last_Price
    last_price = []
    for x in phones_df.last_price:
        last_price.append(x)

    #Current_Price
    curr_price = []
    for x in phones_df.current_price:
        curr_price.append(x)

    #Diferença de preço
    disc_price = []
    for a, b in zip(last_price, curr_price):
        disc_price.append(round(a-b))

    phones_df['discount_price'] = disc_price

    #Porcentagem da diferença de preço
    disc_percent = []
    for a, b in zip(last_price, disc_price):
        disc_percent.append(round((b/a)*100))

    phones_df['discount_percent'] = disc_percent

    return phones_df
