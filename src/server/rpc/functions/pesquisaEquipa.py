import psycopg2


def pesquisaEquipa(pesquisa):

    query = f"""(with j as (SELECT unnest(xpath('/DataSetResults/competitions/competition/teams/team/@Name',xml))::text as Teams_home FROM imported_documents WHERE is_deleted = 'false') SELECT j.Teams_home from j where j.Teams_home like '\"{pesquisa}\"%')"""

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