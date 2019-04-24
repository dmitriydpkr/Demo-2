import psycopg2
import json
import requests
import os
from datetime import date


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

absolute_path_json = BASE_DIR + '/exams2/media/json/parser_raw.json'
absolute_path_media = BASE_DIR + '/exams2/media/good_images/'


def get_json():
    unique_rows, output = [], []
    with open(absolute_path_json) as json_file:
        json_str = json.load(json_file)
        for item in json_str:
            if item['og:product_id'] not in output:
                output.append(item['og:product_id'])
                unique_rows.append(item)
    return unique_rows


def store_good_image(url_image, id_product):
    r = requests.get(url_image)
    with open(absolute_path_media + id_product+'.jpg', 'wb') as f:
        f.write(r.content)
    return id_product


def get_json_data(i):
    t = 1  # 1 = таблица товаров
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
        store_good_image(i['og:images'], i['og:product_id'])
        return product_id_field, category_field, overview_field, currency_field, name_field,provider_name, brand, \
            price_field, photo
    else:
        dict_array = get_dictionary_id_from_db()
        good_id_field = dict_array[product_id_field]
        return good_id_field, average_rating_field, reviews_field, rating_scale_field, price_field, availability_field,\
            standard_price_field, product_id_field, date_field


def update_price_list():
    for row in get_json():
        search_field = 'product_id'
        value_field = row['og:product_id']
        search_update = 'price'
        value_update = float(row['og:price:amount'].replace(',', ''))
        update_table(search_field, value_field, search_update, value_update)


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


def get_dictionary_id_from_db():
    query_set = select_db('main_app_good', "id, product_id")
    dict_id = {}
    for item in query_set:
        dict_id.update({item[1]: item[0]})
    return dict_id


def select_db(table, fields):
    sql_query = "select " + fields + " from public." + table
    cursor.execute(sql_query)
    items = cursor.fetchall()
    return items


def insert_db(table, fields):
    counter = fields.count(',')
    sql_query = " INSERT INTO public." + table + " (" + fields + ")  VALUES (" + '%s,'*counter + '%s)'
    count = 0
    for row in get_json():
        record_to_insert = (get_json_data(row))
        cursor.execute(sql_query, record_to_insert)
        connection.commit()
        count += 1
    return f'{count}, "Record inserted successfully into table'


def update_table(field_search, value_search, field_update, value_set):
    table = 'main_app_good'
    sql_update_query = "Update public." + table + " set " + field_update + " = %s where " + field_search + " = %s"
    cursor.execute(sql_update_query, (value_set, value_search))
    connection.commit()
    return f'Rows update: {cursor.rowcount}'


def main():

    test_connection()

    try:
        table1 = 'main_app_good'
        fields1 = "product_id, category, overview, currency, name, provider_name, brand, price, images"
        insert_db(table1, fields1)

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to insert record into table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    main()
















'''
table1 = 'main_app_good'
fields1 = "product_id, category, overview, currency, name, provider_name, brand, price, images"
test_connection()
insert_db(table1, fields1)



table2 = 'main_app_goodpricerating'
fields2 = "good_id, average_rating, reviews, rating_scale, price, availability, standard_price, product_id, date"
test_connection()
insert_db(table1, fields1)    
    
    
    
# insert_db(table1, fields1)
        # insert_db(table2, fields2)
        update_table('id', '4050', 'price', '25')    
    
    
table2 = 'main_app_goodpricerating'
fields2 = "good_id, average_rating, reviews, rating_scale, price, availability, standard_price, product_id, date"


 update_table('id', '4050', 'price', '25')



 update_price_list()
 
'''

