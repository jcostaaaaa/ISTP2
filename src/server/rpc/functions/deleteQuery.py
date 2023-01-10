import psycopg2

def delete(filename):

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5434",
                                      database="is")



        cursor = connection.cursor()
        cursor.execute("UPDATE imported_documents SET is_deleted = true WHERE file_name = %s", (filename,))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()