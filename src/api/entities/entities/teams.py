import uuid
from datetime import datetime
from entities.db.db_Acess import connection


class Teams:
    def __init__(self, name_team, country_team, id_team=None):
        self.id_team = id_team or uuid.uuid4()
        self.name_team = name_team
        self.country_team = country_team


    @staticmethod
    def get_teams():
        conexao = connection()
        cursor = conexao.cursor()
        cursor.execute("SELECT * from teams")
        result = cursor.fetchall()
        conexao.commit()
        conexao.close()

        return result