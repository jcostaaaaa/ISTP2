import psycopg2


def listarTodasCompetiçoes():

    query = """(select unnest(xpath('/DataSetResults/competitions/competition/@name',xml))::text as Competition from imported_documents where is_deleted = 'false')"""

    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5434",
                                      database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        x = cursor.fetchall()
        connection.commit()



    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return x