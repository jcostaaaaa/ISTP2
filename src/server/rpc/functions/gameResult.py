import psycopg2


def gameResult(competition,team,date):
    query = f"SELECT unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team[@Name=\"{team}\"]/games/game[@Date=\"{date}\"] ', xml))::text as JogosCompData FROM imported_documents WHERE is_deleted = 'false';"

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
