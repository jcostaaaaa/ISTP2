import uuid
from datetime import datetime
from entities.db.db_Acess import connection


class Competition:
    def __init__(self, name, id_comp=None):
        self.id_comp = id_comp or uuid.uuid4()
        self.name = name



    @staticmethod
    def get_competition():
        conexao = connection()
        cursor = conexao.cursor()
        cursor.execute("SELECT * from competition")
        result = cursor.fetchall()
        conexao.commit()
        conexao.close()

        return result