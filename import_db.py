import psycopg2
import json
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_json():

    file_name = BASE_DIR + '/exams2/ParserJson.txt'

    with open(file_name) as json_file:
        json_str = json.load(json_file)

    return json_str


def get_json_data(i):
    product_id_field = i['og:product_id']
    type_good_field = i['og:type']
    category_field = i['category']
    overview_field = i['overview']
    if i['og:title']:
        name_field = str(i['og:title'])
    else:
        name_field = 'na'
    if i['og:price:currency']:
        currency_field = i['og:price:currency']
    else:
        currency_field = 'na'
    provider_name = i['og:provider_name']
    brand = i['og:brand']
    price_field = float(i['og:price:amount'].replace(',', ''))
    photo = 'good_images/' + i['og:product_id']+'.jpg'

    absolute_path_media = BASE_DIR + '/exams2/media/good_images/'
    r = requests.get(i['og:images'])

    with open(absolute_path_media + i['og:product_id']+'.jpg', 'wb') as f:
        f.write(r.content)

    return product_id_field, type_good_field, category_field, overview_field, currency_field, name_field, \
        provider_name, brand, price_field, photo


def import_to_db():

    global connection, cursor, connection
    try:
        connection = psycopg2.connect(user="ukrainer",
                                      password="ze2019",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="godds_db")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO public.main_app_good (product_id, type_good, category, overview,
        currency, name, provider_name, brand, price, images) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        count = 0
        for ix in get_json():
            record_to_insert = (get_json_data(ix))
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count += 1
            print(count)
        print(count, "Record inserted successfully into public.main_app_good table")
    except (Exception, psycopg2.Error) as error:
        if connection:

            print("Failed to insert record into public.main_app_good table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


import_to_db()

