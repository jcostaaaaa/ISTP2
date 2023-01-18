import sys

import psycopg2
from flask import Flask, jsonify

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


def drawByCompetition(competition):
    print(competition)
    query = f"""(with j as (SELECT unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/HomeGoals/text()', xml))::text as Goals_Home,
             unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/AwayGoals/text()', xml))::text as Goals_Away ,
                    unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/@Name', xml))::text as Home_Team,
                       unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/AwayTeam/text()', xml))::text as Away_Team
                             FROM imported_documents WHERE is_imported = true) select count(*) as Numero_Empates FROM j where j.Goals_Home = j.Goals_Away)"""

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        jogos = cursor.fetchall()
        connection.commit()
        return jsonify({'draws': jogos}), 200


    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def gameResult(competition, team, date):
    query = f"SELECT unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team[@Name=\"{team}\"]/games/game[@Date=\"{date}\"] ', xml))::text as JogosCompData FROM imported_documents WHERE is_imported = 'true';"

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

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


def gamesByCompetition(competition):
    query = f"""(SELECT unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/HomeGoals/text()', xml))::text as Goals_Home,
                 unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/AwayGoals/text()', xml))::text as Goals_Away ,
                        unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/@Name', xml))::text as Home_Team,
                           unnest(xpath('/DataSetResults/competitions/competition[@name=\"{competition}\"]/teams/team/games/game/AwayTeam/text()', xml))::text as Away_Team
                                 FROM imported_documents WHERE is_imported = true)"""

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        jogos = cursor.fetchall()
        connection.commit()
        return jsonify({'games': jogos}), 200


    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def jogosPortugal(data):
    query = f"""(SELECT homeTeam,awayTeam,home ||'-'||  away as score ,date from (select
       unnest(xpath('/DataSetResults/competitions/competition[@name=''uruguay'']/teams/team/@Name',xml))::text as homeTeam,
       unnest(xpath('/DataSetResults/competitions/competition[@name=''uruguay'']/teams/team/games/game/AwayTeam/text()',xml))::text as awayTeam,
       unnest(xpath('/DataSetResults/competitions/competition[@name=''uruguay'']/teams/team/games/game/HomeGoals/text()',xml))::text::int as home,
        unnest(xpath('/DataSetResults/competitions/competition[@name=''uruguay'']/teams/team/games/game/AwayGoals/text()',xml))::text::int as away,
        unnest(xpath('/DataSetResults/competitions/competition[@name=''uruguay'']/teams/team/games/game/@Date',xml))::text as date FROM imported_documents WHERE
        is_imported = true group by homeTeam,awayTeam,home,away,date) as g where (g.date > '''\"{data}\"''' ) group by g.homeTeam,g.awayTeam,g.home,g.away,g.date)"""

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        jogos = cursor.fetchall()
        connection.commit()
        return jsonify({'gamePor': jogos}), 200


    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def listarTodasCompetiçoes():
    query = """(select unnest(xpath('/DataSetResults/competitions/competition/@name',xml))::text as Competition from imported_documents where is_imported = 'true')"""

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        jogos = cursor.fetchall()
        connection.commit()
        return jsonify({'competitions': jogos}), 200




    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def pesquisaEquipa(pesquisa):
    query = f"""(with j as (SELECT unnest(xpath('/DataSetResults/competitions/competition/teams/team/@Name',xml))::text as Teams_home FROM imported_documents WHERE is_deleted = 'false') SELECT j.Teams_home from j where j.Teams_home like '\"{pesquisa}\"%')"""

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")
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


def procurarJogosMaisGolos():
    query = f"""(select unnest(array_cat(xpath('/DataSetResults/competitions/competition/teams/team/games/game[HomeGoals>AwayGoals]/HomeGoals/text()',xml)::text[],
    xpath('/DataSetResults/competitions/competition/teams/team/games/game[AwayGoals>HomeGoals]/ AwayGoals/text()',xml)::text[])) as Golos_Marcados,count(*) as Vitorias from imported_documents where is_imported = true group by Golos_Marcados order by vitorias asc)"""

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        jogos = cursor.fetchall()
        connection.commit()
        return jsonify({'procJogos': jogos}), 200


    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def top10JogoscomGolos(comp, data_ini, data_fim):
    query = f"""(SELECT homeTeam,awayTeam,home ||'-'||  away as score ,sum(home+away) as sumGoals,date from (select unnest(xpath('/DataSetResults/competitions/competition[@name=\"{comp}\"]/teams/team/@Name',xml))::text as homeTeam,
       unnest(xpath('/DataSetResults/competitions/competition[@name=\"{comp}\"]/teams/team/games/game/AwayTeam/text()',xml))::text as awayTeam,
       unnest(xpath('/DataSetResults/competitions/competition[@name=\"{comp}\"]/teams/team/games/game/HomeGoals/text()',xml))::text::int as home,
        unnest(xpath('/DataSetResults/competitions/competition[@name=\"{comp}\"]/teams/team/games/game/AwayGoals/text()',xml))::text::int as away,
        unnest(xpath('/DataSetResults/competitions/competition[@name=\"{comp}\"]/teams/team/games/game/@Date',xml))::text as date FROM imported_documents WHERE
        is_deleted = 'false' group by homeTeam,awayTeam,home,away,date) as g where (g.date between '\"{data_ini}\"' and '\"{data_fim}\"') group by g.homeTeam,g.awayTeam,g.home,g.away,g.date order by sumGoals DESC limit 10)"""

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", database="is")

        cursor = connection.cursor()
        cursor.execute(query)
        jogos = cursor.fetchall()
        connection.commit()
        return jsonify({'top10': jogos}), 200



    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return jogos


@app.route('/api/allcompetitions', methods=['GET'])
def get_best_players():
    return listarTodasCompetiçoes()


@app.route('/api/getgolosjogo', methods=['GET'])
def get_golos_jogo():
    return procurarJogosMaisGolos()


@app.route('/api/getdrawscomp/<competition>', methods=['GET'])
def get_draws_comp(competition):
    return drawByCompetition(competition)

@app.route('/api/getgamescomp/<competition>', methods=['GET'])
def get_games_comp(competition):
    return gamesByCompetition(competition)

@app.route('/api/gamesPor/<date>', methods=['GET'])
def get_games_por(date):
    return jogosPortugal(date)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
