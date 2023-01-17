# # import csv
# # import xml.dom.minidom as md
# # import xml.etree.ElementTree as ET
# #
# # from utils.reader import CSVReader
# # from entities.country import Country
# # from entities.team import Team
# # from entities.player import Player
# #
# #
# # class CSVtoXMLConverter:
# #
# #     def __init__(self, path):
# #         self._reader = CSVReader(path)
# #
# #     def to_xml(self):
# #         # read countries
# #         countries = self._reader.read_entities(
# #             attr="nationality",
# #             builder=lambda row: Country(row["nationality"])
# #         )
# #
# #         # read teams
# #         teams = self._reader.read_entities(
# #             attr="Current Club",
# #             builder=lambda row: Team(row["Current Club"])
# #         )
# #
# #         # read players
# #
# #         def after_creating_player(player, row):
# #             # add the player to the appropriate team
# #             teams[row["Current Club"]].add_player(player)
# #
# #         self._reader.read_entities(
# #             attr="full_name",
# #             builder=lambda row: Player(
# #                 name=row["full_name"],
# #                 age=row["age"],
# #                 country=countries[row["nationality"]]
# #             ),
# #             after_create=after_creating_player
# #         )
# #
# #         # generate the final xml
# #         root_el = ET.Element("Football")
# #
# #         teams_el = ET.Element("Teams")
# #         for team in teams.values():
# #             teams_el.append(team.to_xml())
# #
# #         countries_el = ET.Element("Countries")
# #         for country in countries.values():
# #             countries_el.append(country.to_xml())
# #
# #         root_el.append(teams_el)
# #         root_el.append(countries_el)
# #
# #         return root_el
# #
# #     def to_xml_str(self):
# #         xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
# #         dom = md.parseString(xml_str)
# #         return dom.toprettyxml()
# #
#
#
# from .coordinates import get_data_api
# from xml.etree.ElementTree import SubElement, Element, ElementTree
#
#
# def converter(src: str, out: str):
#     f = format_data(src)
#
#     root = Element('DataSetResults')
#     competitions_el = SubElement(root, 'competitions')
#
#     for idx, (competition, values) in enumerate(f.items()):
#         competition_el = SubElement(competitions_el, 'competition', {
#             'name': competition,
#         })
#
#         teams_el = SubElement(competition_el, 'teams')
#         for team in values['teams']:
#             team_el = SubElement(teams_el, 'team', {
#                 'Name': team['Name'],
#                 'Code': team['Code'],
#                 'Coordinates': team['Coordinates']
#             })
#
#             games_el = SubElement(team_el, 'games')
#             for game in team['games']:
#                 game_el = SubElement(games_el, 'game', {
#                     'Date': game['Date'],
#                 })
#
#                 SubElement(game_el, 'HomeGoals').text = game['HomeGoals']
#                 SubElement(game_el, 'AwayGoals').text = game['AwayGoals']
#                 SubElement(game_el, 'AwayTeam').text = game['AwayTeam']
#                 SubElement(game_el, 'AwayCountry').text = game['AwayCountry']
#                 SubElement(game_el, 'AwayCode').text = game['AwayCode']
#
#     et = ElementTree(root)
#     et.write(out)

import csv

from .coordinates import get_data_api
from xml.etree.ElementTree import SubElement, Element, ElementTree


def converter(src: str, out: str):
    f = format_data(src)

    root = Element('DataSetResults')
    competitions_el = SubElement(root, 'competitions')

    for idx, (competition, values) in enumerate(f.items()):
        competition_el = SubElement(competitions_el, 'competition', {
            'name': competition,
        })

        teams_el = SubElement(competition_el, 'teams')
        for team in values['teams']:
            team_el = SubElement(teams_el, 'team', {
                'Name': team['Name'],
                'Code': team['Code'],
                'Coordinates': team['Coordinates']
            })

            games_el = SubElement(team_el, 'games')
            for game in team['games']:
                game_el = SubElement(games_el, 'game', {
                    'Date': game['Date'],
                })

                SubElement(game_el, 'HomeGoals').text = game['HomeGoals']
                SubElement(game_el, 'AwayGoals').text = game['AwayGoals']
                SubElement(game_el, 'AwayTeam').text = game['AwayTeam']
                SubElement(game_el, 'AwayCountry').text = game['AwayCountry']
                SubElement(game_el, 'AwayCode').text = game['AwayCode']

    et = ElementTree(root)
    et.write(out)


def format_data(src):
    with open(src) as f:
        csv_f = csv.DictReader(f)
        data = {}

        for idx, row in enumerate(csv_f):
            competition = row['competition']
            if competition not in data:
                data[competition] = {
                    'teams': []
                }
            team_dict = next(filter(lambda homeTeam: homeTeam['Name'] == row['home'], data[competition]['teams']), None)
            if team_dict is None:
                team_dict = {
                    'Name': row['home'],
                    'Code': row['home_code'],
                    'Coordinates': get_data_api(row['home_country']),
                    'games': [],
                }
                data[competition]['teams'].append(team_dict)
            team_dict['games'].append({
                'AwayTeam': row['away'],
                'HomeGoals': row['gh'],
                'AwayGoals': row['ga'],
                'AwayCountry': row['away_country'],
                'AwayCode': row['away_code'],
                'Date': row['date'],

            })

    return data
