import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


DOMAIN = 'https://www.avito.ru'
# запросы похожие будут записываться, для уменьшения нагрузки,
# а также чтобы исключить повторный парсинг
# по хорошему можно и нужно в будущем добавить функцию очистки временных файлов (к примеру через 2 дня удалять)
# и до начала парсинга проверять дату и время создания tmp-f, если  файл давний,
# то парсинг выполнять снова, а старый удалить
PATH_TMP = 'cache/'  # папка временного хранения html объявлений
PATH_DOCS = 'docs/'  # папка временного хранения xlsx объявлений
PATH_IMAGES = 'cache_img/'

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
    file_search = f"{PATH_TMP}{request.replace(' ', '')}.html"
    if not os.path.exists(file_search):
        src = requests.get(url, headers=headers).text
        with open(file_search, 'w', encoding='utf-8') as f:
            f.write(src)
    else:
        with open(file_search, 'r', encoding='utf-8') as f:
            src = f.read()
    return src


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


def to_parse(req, tmp_dict):
    response = get_search_html(req)
    soup = BeautifulSoup(response, 'lxml')
    tmp_dict = parsing_page(soup=soup, tmp_dict=tmp_dict)
    return tmp_dict


def save_to_excel(req, tmp_dict):
    file = f"{PATH_DOCS}{req.replace(' ', '')}.xlsx"
    df_inner = pd.DataFrame(tmp_dict)
    if not os.path.exists(file):
        df_inner.to_excel(file, sheet_name=f'{req}')
        return 0, file, f'Парсинг завершен: создан файл {req}.xlsx'
    else:
        return 1, file, f'Файл {req}.xlsx существует'


def save_img_res(req, tmp_dict):
    file = f"{PATH_IMAGES}{req.replace(' ', '')}.png"
    df_inner = pd.DataFrame(tmp_dict)
    sns.histplot(df_inner['Цена'], kde=True)
    if not os.path.exists(file):
        plt.savefig(file)
        return 0, file
    else:
        return 1, file


if __name__ == '__main__':
    # request = input('Сбор данных с авито по поисковому запросу: ')
    request = 'gtx 1080 ti'  # видеокарта gtx 1080 ti
    df_dict = to_parse(request, df_dict)
    print(save_to_excel(request, df_dict)[2])

    save_img_res(df_dict)

    # Тест анализ
    df = pd.read_excel('docs/gtx1080ti.xlsx')
    print(df.describe()) # 75% объявлений лежит в диапазоне цен до 70000
    sns.histplot(df[(df['Цена'] > 10000) & (df['Цена'] < 100000)]['Цена'], kde=True)
    plt.show()  # отобразить график

