import psycopg2

def procurarJogosMaisGolos():

    query = f"""(select unnest(array_cat(xpath('/DataSetResults/competitions/competition/teams/team/games/game[HomeGoals>AwayGoals]/HomeGoals/text()',xml)::text[],
    xpath('/DataSetResults/competitions/competition/teams/team/games/game[AwayGoals>HomeGoals]/ AwayGoals/text()',xml)::text[])) as Golos_Marcados,count(*) as Vitorias from imported_documents where is_deleted='false' group by Golos_Marcados order by vitorias asc)"""

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
