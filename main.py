import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


DOMAIN = 'https://www.avito.ru'
PATH_TMP = 'temp'  # папка временного хранения html объявлений

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/99.0.4844.82 Safari/537.36 '
}

df_dict = {
    'Название продукта': [],
    'Цена': [],
    'Описание': [],
    'Ссылка': [],
    'Пункт объявления': []
}


# функция формирование главной поисковой страницы, из которой
# в дальнейшем будут вытягиваться объявления
def get_search_html(request: str):
    url = f'{DOMAIN}/rossiya?q={request}'
    file_search = f"{request.replace(' ', '')}.html"
    if not os.path.exists(file_search):
        src = requests.get(url, headers=headers).text
        with open(file_search, 'w', encoding='utf-8') as f:
            f.write(src)
    else:
        with open(file_search, 'r', encoding='utf-8') as f:
            src = f.read()
    return src


# функция парсинга ссылок объявлений из оффлайн html файла
# def get_a_all(soup):
#     links_posters = soup.find('div', {'elementtiming': "bx.catalog.container"}).find_all('a')
#     a_all = []
#     for item in links_posters:
#         if 'user' not in item['href'] and 'login' not in item['href']:
#             a_all.append(f"{DOMAIN}{item['href']}")
#     return a_all


def parsing_page(soup, tmp_dict):
    names = soup.find_all('div', class_="iva-item-titleStep-pdebR")
    prices = soup.find_all('div', class_="iva-item-priceStep-uq2CQ")
    descriptions = soup.find_all('meta', {"itemprop": "description"})
    links = soup.find_all('div', class_="iva-item-titleStep-pdebR")
    regions = soup.find_all('div', class_="geo-root-zPwRk iva-item-geo-_Owyg")
    for name, price, description, link, region in zip(names, prices, descriptions, links, regions):
        tmp_dict['Название продукта'].append(name.find('h3').text)
        price_tmp = price.find('meta', {"itemprop": "price"})['content']
        tmp_dict['Цена'].append(float(price_tmp) if price_tmp.isdigit() else None)
        tmp_dict['Описание'].append(description['content'])
        tmp_dict['Ссылка'].append(f"{DOMAIN}{link.find('a')['href']}")
        tmp_dict['Пункт объявления'].append(region.find('span').text)

    return tmp_dict


if __name__ == '__main__':
    request = input('Сбор данных с авито по поисковому запросу: ')
    # request = 'gtx 1080 ti'
    response = get_search_html(request)
    soup = BeautifulSoup(response, 'lxml')
    df_dict = parsing_page(soup=soup, tmp_dict=df_dict)
    df = pd.DataFrame(df_dict)
    df.to_excel(f"{request.replace(' ', '')}.xlsx", sheet_name=f'{request}')
    print(f'Парсинг завершен: создан файл {request}.xlsx')

    # Тест анализ
    df = pd.read_excel('gtx1080ti.xlsx')
    print(df.describe()) # 75% объявлений лежит в диапазоне цен до 70000
    sns.histplot(df[(df['Цена'] > 10000) & (df['Цена'] < 100000)]['Цена'], kde=True)
    plt.show() # отобразить график

