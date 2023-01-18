import sys
import time

import psycopg2 as psycopg2

from src.daemon.importer.utils.coordinates import get_data_api

if __name__ == "__main__":

    connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT g.id_game as id, t.country_team as country FROM teams t, game g where t.id_team = g.id_home_team and g.geo is null ",
        )
        result = cursor.fetchall()

    for id, country in result:
        coords = get_data_api(country)
        if coords is not None:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE game SET geo = ST_SetSRID(ST_MakePoint(%s, %s),4326) where id_game = %s",
                               (float(coords[0]), float(coords[1]), id))
                connection.commit()

    connection.close()