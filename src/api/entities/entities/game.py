import uuid
from datetime import datetime
from entities.db.db_Acess import connection


class Game:
    def __init__(self, gh, ga, date, geo, id_home_team, id_away_team, id_comp, id_game=None):
        self.id_game = id_game or uuid.uuid4()
        self.id_home_team = id_home_team #or uuid.uuid4()
        self.id_away_team = id_away_team #or uuid.uuid4()
        self.id_comp = id_comp #or uuid.uuid4()
        self.gh = gh
        self.ga = ga
        self.date = date
        self.geo = geo

    @staticmethod
    def get_games():
        conexao = connection()
        cursor = conexao.cursor()
        cursor.execute("SELECT g.id_game,(select t.name_team from teams t where g.id_home_team=t.id_team) as TeamHome,(select t.name_team from teams t where g.id_away_team=t.id_team) as AwayTeam,g.gh,g.ga,g.date,g.geo,(select c.name from competition c where c.id_comp=g.id_comp) as TeamHome from game g")
        result = cursor.fetchall()
        conexao.commit()
        conexao.close()

        return result
