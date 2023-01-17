import sys
from flask import Flask, jsonify, request

from entities.competition import Competition
from entities.teams import Teams
from entities.game import Game



PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

# set of all teams
# !TODO: replace by database access

@app.route('/api/competitions', methods=['GET'])
def get_competitions():
    result = Competition.get_competition()
    return jsonify({'competitions': result}), 200


@app.route('/api/teams', methods=['GET'])
def get_teams():
    result = Teams.get_teams()

    return jsonify({'teams': result}), 200

@app.route('/api/games', methods=['GET'])
def get_games():
    result = Game.get_games()

    return jsonify({'games': result}), 200





# @app.route('/api/competitions/', methods=['POST'])
# def create_competition():
#     data = request.get_json()
#     competition = Competition(name=data['name'])
#     #competitions.append(competition)
#     return jsonify(competition.__dict__), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)