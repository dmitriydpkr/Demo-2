import psycopg2
import json
import requests
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
absolute_path_json = BASE_DIR + '/exams2/sites5.json'

t = 1   # 1 = таблица товаров


def get_json():
    with open(absolute_path_json) as json_file:
        json_str = json.load(json_file)
    return json_str


def store_good_image(url_image, id_product):
    absolute_path_media = BASE_DIR + '/exams2/media/good_images/'
    r = requests.get(url_image)
    with open(absolute_path_media + id_product+'.jpg', 'wb') as f:
        f.write(r.content)
    return id_product


def get_json_data(i):

    category_field = i['category']
    overview_field = i['overview']
    product_id_field = i['og:product_id']
    availability_field = str(i['og:availability'])
    average_rating_field = float(i['og:rating'])
    standard_price_field = float(i['og:standard_price'].replace(',', ''))
    reviews_field = int(i['og:rating_count'])
    rating_scale_field = float(i['og:rating_scale'])
    date_field = date.today()
    provider_name = i['og:provider_name']
    brand = i['og:brand']
    price_field = float(i['og:price:amount'].replace(',', ''))
    photo = 'good_images/' + i['og:product_id'] + '.jpg'
    name_field = str(i['og:title'])
    currency_field = i['og:price:currency']
    store_good_image(i['og:images'], i['og:product_id'])

    if t == 1:
        return product_id_field, category_field, overview_field, currency_field, name_field, \
             provider_name, brand, price_field, photo
    else:
        return average_rating_field, reviews_field, rating_scale_field, price_field, availability_field,\
            standard_price_field, product_id_field, date_field


def test_connection():
    global connection, cursor
    try:
        connection = psycopg2.connect(user="ukrainer",
                                      password="ze2019",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="godds_db")
        cursor = connection.cursor()
        print('Connection success')
        return cursor
    except (Exception, psycopg2.Error) as error:
        print(error)


def import_to_db():
    if t == 1:
        table = 'main_app_good'
        fields = "product_id, category, overview, currency, name, provider_name, brand, price, images"
    else:
        table = 'main_app_goodpricerating'
        fields = "average_rating, reviews, rating_scale, price, availability, standard_price, product_id, date"
    counter = fields.count(',')
    global connection, cursor
    try:
        cursor = test_connection()

        postgres_insert_query = " INSERT INTO public." + table + " (" + fields + ")  VALUES (" + '%s,'*counter + '%s)'

        count = 0
        for row in get_json():
            record_to_insert = (get_json_data(row))
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count += 1

        print(count, "Record inserted successfully into table")
    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to insert record into table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def update_table(field_search, value_search, field_update, value_set):
    table = 'main_app_good'

    global connection, cursor
    try:
        cursor = test_connection()
        sql_update_query = "Update public." + table + " set " + field_update + " = %s where " + field_search + " = %s"
        cursor.execute(sql_update_query, (value_set, value_search))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


import_to_db()
# update_table('product_id', '938', 'name', 'fdssdfsda')

'''
for row in get_json():
    search_field = 'product_id'
    value_field = row['og:product_id']
    search_update = 'price'
    value_update = float(row['og:price:amount'].replace(',', ''))
    update_table(search_field, value_field, search_update, value_update)

'''

