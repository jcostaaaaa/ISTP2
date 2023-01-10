import psycopg2

def gamesByCompetition(competition):
    query = f"""(SELECT unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/HomeGoals/text()', xml))::text as Goals_Home,
                 unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/AwayGoals/text()', xml))::text as Goals_Away ,
                        unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/@Name', xml))::text as Home_Team,
                           unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/AwayTeam/text()', xml))::text as Away_Team
                                 FROM imported_documents WHERE is_deleted = 'false')"""

    #
    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="localhost",
                                      port="5434",
                                      database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        jogos = cursor.fetchall()
        connection.commit()



    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return jogos
