import psycopg2


def update_table(name, price):

    global connection, cursor, connection
    try:
        connection = psycopg2.connect(user="ukrainer",
                                      password="ze2019",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="godds_db")
        cursor = connection.cursor()

        print("Table Before updating record ")
        sql_select_query = """select * from public.firstapp_good where name = %s"""
        cursor.execute(sql_select_query, (name, ))
        record = cursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = """Update public.firstapp_good set price = %s where name = %s"""
        cursor.execute(sql_update_query, (price, name))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        print("Table After updating record ")
        sql_select_query = """select * from public.firstapp_good where name = %s"""
        cursor.execute(sql_select_query, (name,))
        record = cursor.fetchone()
        print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


name = "Батончик"
price = 277
update_table(name, price)
