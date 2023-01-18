import sys

import psycopg2

from flask import Flask

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/markers', methods=['GET'])
def get_markers():
    connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT g.id_game,"
        "(select t.name_team from teams t where g.id_home_team=t.id_team) as TeamHome,"
        "(select t.name_team from teams t where g.id_away_team=t.id_team) as AwayTeam,"
        "g.gh,g.ga,g.date,"
        "ST_X(geo) as latitude, ST_Y(geo) as longitude,"
        "(select c.name from competition c where c.id_comp=g.id_comp) as Competetition from game g")

    games = []

    for row in cursor:
        games.append({
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row[6], row[7]]
            },
            "properties": {
                "id": row[0],
                "hometeam": row[1],
                "awayteam": row[2],
                "goalshome": row[3],
                "goalsaway": row[4],
                "date": row[5],
                "competition": row[8],
                "imgUrl": "https://imagensemoldes.com.br/wp-content/uploads/2018/06/Futebol-Bola-de-Futebol-PNG.png"

            }
        })

    cursor.close()
    connection.close()
    return games

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)