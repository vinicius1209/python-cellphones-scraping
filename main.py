from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import json
import time

def create_df():

    num_pages = input('Quantas páginas desejas buscar históricos de celulares?')
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

    for page in range(1, int(num_pages)+1):
        url = 'https://www.ofertaesperta.com/categoria/celulares-e-smartphones?page=' + str(page)
        response = get(url, headers=headers)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        phones_containers = html_soup.find_all('div', class_="cards")
        phones_cards = phones_containers[0].find_all('div', class_="card-col")

        for phones in phones_cards:
            id = phones.find_all('div')[0].get('id').replace('card-', '')
            print('Gerando para o ID: ' + str(id))

            response_json = get_all_info_by_api(id)
            if 'cupon' in response_json:
                cupom_obj = response_json["cupon"]
            else:
                cupom_obj = {'code': '-', "title": '-'}

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

    phones_df = pd.DataFrame({
        "id": ids,
        "image": images,
        "phone_title": titles,
        "last_price": last_prices,
        "current_price": current_prices,
        "payment_format": payment_formats,
        "cupom_code": cupons_codes,
        "cupom_title": cupons_titles,
        "store": stores,
    })

    print('Salvando em arquivo CSV...')

    phones_df.to_csv("phones.csv", sep='\t', encoding='utf-8')

    """ OLD WAY TO GET INFORMATIONS BY HTML
    #Id da promoção
    id = phones_cards[0].find_all('div')[0].get('id').replace('card-', '')
    print(id)
    #Preço anterior
    print(phones_cards[0].find(class_="offer-previous-price").find_all('p')[0].text.replace(' ', ''))
    #Preço atual
    print(phones_cards[0].find(class_="offer-card-price").text)
    #Método de pagamento
    print(phones_cards[0].find(class_="offer-payment-format").text)
    """

def get_all_info_by_api(id):

    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    url = 'https://www.ofertaesperta.com/api/offers/' + str(id)
    #time.sleep(3)
    response = get(url, headers=headers)
    response_json = json.loads(response.text)

    return response_json

create_df()