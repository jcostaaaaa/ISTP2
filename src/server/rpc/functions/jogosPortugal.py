import psycopg2

def jogosPortugal(data):

    query = f"""(SELECT homeTeam,awayTeam,home ||'-'||  away as score ,date from (select
       unnest(xpath('/DataSetResults/competitions/competition[@name=''portugal'']/teams/team/@Name',xml))::text as homeTeam,
       unnest(xpath('/DataSetResults/competitions/competition[@name=''portugal'']/teams/team/games/game/AwayTeam/text()',xml))::text as awayTeam,
       unnest(xpath('/DataSetResults/competitions/competition[@name=''portugal'']/teams/team/games/game/HomeGoals/text()',xml))::text::int as home,
        unnest(xpath('/DataSetResults/competitions/competition[@name=''portugal'']/teams/team/games/game/AwayGoals/text()',xml))::text::int as away,
        unnest(xpath('/DataSetResults/competitions/competition[@name=''portugal'']/teams/team/games/game/@Date',xml))::text as date FROM imported_documents WHERE
        is_deleted = 'false' group by homeTeam,awayTeam,home,away,date) as g where (g.date > '''\"{data}\"''' ) group by g.homeTeam,g.awayTeam,g.home,g.away,g.date)"""

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