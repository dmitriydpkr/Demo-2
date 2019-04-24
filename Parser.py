from multiprocessing import Pool
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os
from os.path import join
import import_db

url = 'https://www.iherb.com'
absolute_path_tmp_json = import_db.BASE_DIR + '/exams2/media/json/'
output_parser_json = absolute_path_tmp_json + 'parser_raw.json'
meta_items = ['og:provider_name', 'og:title', 'og:type', 'og:price:amount', 'og:price:currency', 'og:brand',
              'og:product_id', 'og:availability', 'og:standard_price', 'og:rating', 'og:rating_scale',
              'og:rating_count', 'og:images', 'og:images', 'og:images']


def get_html(source):
    r = requests.get(source)
    return r.text


def get_category_list():
    result = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('ul', class_="nav-item-list").find_all('li')
    for div in divs:
        href_category = div.find('a', attrs={'data-ga-event': 'click'}).get('href')
        href_category = href_category.replace('//ua.', '')
        if '/c/' in href_category:
            result.append('https://www.' + href_category)
    return result


def get_href_goods():
    result = []
    for category in get_category_list():
        count = 1
        end_link = ''
        while count < 2:
            html = get_html(str(category) + end_link)
            soup = BeautifulSoup(html, 'lxml')
            divs = soup.find_all('div', class_='product ga-product col-xs-12 col-sm-12 col-md-8 col-lg-6')
            for div in divs:
                href_good = div.find('a',  class_="product-image").get('href')
                result.append(href_good)
            time.sleep(1)
            count += 1
            end_link = f'?p={count}'
    return set(result)


def get_properties_goods(link):
    html = get_html(link)
    soup = BeautifulSoup(html, 'lxml')
    tmp_array = {}
    result_properties = []

    try:
        desc_g = []
        for item in meta_items:
            divs = soup.find('meta', attrs={'property': str(item)})
            content_good = divs.get('content')
            tmp_array.update({item: content_good})

        divs = soup.find('div', attrs={'itemprop': 'description'}).find_all('li')
        for div in divs:
            overview_good = div.text
            desc_g.append(overview_good)
            desc_g.append('\n')
        my_result = ''.join(desc_g)
        tmp_array.update({'overview': my_result})

        category_name = soup.find('meta', attrs={'itemprop': 'category'}).get('content')
        tmp_array.update({'category': category_name})
        result_properties.append(tmp_array)
        return write_json(tmp_array)
    except Exception:
        print('The page don"t have such meta tags as other pages', '--', link)
    # print(result_properties)


def write_json(data):
    name = random.randint(-100000, 1000000)
    file_name = absolute_path_tmp_json + str(name) + '.json'
    my_file = open(file_name, mode='w')
    time.sleep(1)
    json.dump(data, my_file)
    my_file.close()
    return file_name


def get_list_files():
    my_txt = []
    for root, dirs, files in os.walk(absolute_path_tmp_json):
        my_txt.extend([join(root, file) for file in files if file.endswith('json')])
        dirs.clear()
    return my_txt


def get_free_json():
    json_array = []
    for i in get_list_files():
        json_doc = open(i, mode='r')
        json_str = json.load(json_doc)
        json_array.append(json_str)
        json_doc.close()
        os.remove(i)
    my_file = open(output_parser_json, mode='w')
    json.dump(json_array, my_file)
    print(len(json_array))
    my_file.close()


def main():
    start = datetime.now()

    all_links = get_href_goods()
    with Pool(30) as p:
        p.map(get_properties_goods, all_links)
    get_free_json()

    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()
