import sys
import time

import psycopg2
from psycopg2 import OperationalError

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        cursorCheckDataBase = db_org.cursor()
        cursorCheckDataBase.execute("select count(*) from imported_documents where is_imported=false")
        count = cursorCheckDataBase.fetchone()

        if count[0] > 0:
            print("We have new imported files in the database!!")
        else:
            print("We already imported all the files to the database")

        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db

        cursorSelectImportedDocuments = db_org.cursor()
        cursorSelectImportedDocuments.execute("select id from imported_documents where is_imported= false ")
        idsImportedDocuments = cursorSelectImportedDocuments.fetchall();

        #     # !TODO: 3- Execute INSERT queries in the destination db

        for id1 in idsImportedDocuments:
            # COMPETITIONS CURSOR
            cursorOrigemCompetitions = db_org.cursor()
            cursorOrigemCompetitions.execute(

                "select unnest(xpath('DataSetResults/competitions/competition/@name',xml)):: text as Competition"

                " from imported_documents where id= %s",
                (id1,))
            competitions = cursorOrigemCompetitions.fetchall()
            cursorOrigemCompetitions.close()

            # TEAMS HOME CURSOR
            cursorOrigemTeamsHome = db_org.cursor()
            cursorOrigemTeamsHome.execute(
                "select unnest(xpath('DataSetResults/competitions/competition/teams/team/@Name',xml)):: text as Teams,"
                "unnest(xpath('DataSetResults/competitions/competition/teams/team/@Code',xml))::text as codeHomeTeam"
                " from imported_documents where id=%s",
                (id1,))
            homeTeams = cursorOrigemTeamsHome.fetchall()
            cursorOrigemTeamsHome.close()

            # TEAMS AWAY CURSOR
            cursorOrigemTeamsAway = db_org.cursor()
            cursorOrigemTeamsAway.execute(
                "select unnest(xpath('DataSetResults/competitions/competition/teams/team/games/game/AwayTeam/text()',xml)):: text as Teams,"
                "unnest(xpath('DataSetResults/competitions/competition/teams/team/games/game/AwayCode/text()',"
                "xml))::text as codeAwayTeam "
                " from imported_documents where id=%s",
                (id1,))
            awayTeams = cursorOrigemTeamsAway.fetchall()
            cursorOrigemTeamsAway.close()

            # GAMES CURSOR
            cursorOrigemGames = db_org.cursor()
            cursorOrigemGames.execute(
              """ 
              with competitions as (
    select
           unnest(xpath('DataSetResults/competitions/competition',xml)) as competition
    from imported_documents
    where id=%s

),teams as (
   select
          (xpath('/competition/@name',competition))[1] ::text as competition ,
          unnest(xpath('/competition/teams/team',competition)) as team
   from competitions


), games as (
    select
           competition,
           (xpath('/team/@Name',team))[1] ::text as homeTeam ,
            unnest(xpath('/team/games/game',team)) as game
    from teams
)
select
        competition,
       homeTeam,
       (xpath('/game/AwayTeam/text()',game))[1] :: text as awayTeam,
       (xpath('/game/HomeGoals/text()',game))[1] :: text as homeGoals,
       (xpath('/game/AwayGoals/text()',game))[1] :: text as awayGoals,
       (xpath('/game/@Date',game))[1] :: text as Date
from games
              """,
                (id1,))
            games = cursorOrigemGames.fetchall()
            cursorOrigemGames.close()

            # !TODO: 3- Execute INSERT queries in the destination db
            cursorDestino = db_dst.cursor()
            # COMPETITIONS INSERT
            for competition in competitions:
                cursorDestino.execute("SELECT id_comp FROM competition WHERE name = %s", (competition[0],))
                if cursorDestino.fetchone():
                    print("Já existe esta competição")
                else:
                    cursorDestino.execute("INSERT INTO competition (name) VALUES (%s)", (competition[0],))
            # HOMETEAM INSERT
            for homeTeam in homeTeams:
                cursorDestino.execute("SELECT id_team FROM teams WHERE name_team = %s", (homeTeam[0],))
                if cursorDestino.fetchone():
                    print("Já existe esta equipa")
                else:
                    cursorDestino.execute("Insert into teams (name_team,country_team) VALUES (%s,%s)",
                                          (homeTeam[0], homeTeam[1]))
            # AWAYTEAM INSERT
            for awayTeam in awayTeams:
                cursorDestino.execute("SELECT id_team FROM teams WHERE name_team = %s", (awayTeam[0],))
                if cursorDestino.fetchone():
                    print("Já existe esta equipa")
                else:
                    cursorDestino.execute("INSERT INTO teams (name_team,country_team) VALUES (%s,%s)",
                                          (awayTeam[0], awayTeam[1]))
            # GAME INSERT
            for game in games:

                cursorDestino.execute(
                    "Insert into game(id_home_team, id_away_team, gh, ga, date, id_comp) VALUES ("
                    "(select id_team from teams where name_team = %s limit 1) "
                    ",(select id_team from teams where name_team = %s limit 1),%s,%s,"
                    "%s,(select id_comp from competition where name= %s limit 1))",
                    (game[1], game[2], game[3], game[4], game[5], game[0]))

                # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
            #          Change the db structure if needed.
            cursor2 = db_org.cursor()
            cursor2.execute("UPDATE imported_documents set is_imported = true where id=%s", (id1,))
            db_org.commit()
            cursorDestino.close()
        db_dst.commit()

        time.sleep(POLLING_FREQ)
