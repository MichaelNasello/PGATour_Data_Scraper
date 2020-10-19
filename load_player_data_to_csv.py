import csv
import json
import os
import urllib.request

import requests
from bs4 import BeautifulSoup


class GetPlayerData:

    def __init__(self, year, player, csv_path):

        self.year = year
        self.player_name = player

        self.base_url = 'https://www.pgatour.com/players/player.'
        self.url = None

        if not os.path.exists(csv_path):
            raise IOError('File cannot be found')
        else:
            self.csv_path = csv_path

        self.players_with_ids = {}
        self.categories = ['OFF THE TEE', 'APPROACH THE GREEN', 'AROUND THE GREEN', 'PUTTING', 'TEE TO GREEN', 'TOTAL']

        self.page = None
        self.soup = None

    def read_csv(self):

        with open(self.csv_path, newline='') as csvfile:

            reader = csv.reader(csvfile)
            for row in reader:

                if not row:
                    continue

                self.players_with_ids[row[0]] = row[1]

    def load_from_json(self):

        player_id = self.players_with_ids[self.player_name]
        url = 'https://statdata-api-prod.pgatour.com/api/clientfile/YtdPlayerStatsArchive?P_ID={}&YEAR={}&format=json'.format(player_id, self.year)

        data_dict = {}

        with urllib.request.urlopen(url) as url:

            data = json.loads(url.read().decode())

            for i in range(6):
                data_dict[self.categories[i]] = data['plrs'][0]['years'][0]['tours'][0]['statCats'][0]['stats'][i]['value']

        return data_dict

    def write_data_dict_to_csv(self, data_dict):

        save_dir = self.player_name.replace(' ', '')
        save_folder = self.player_name.replace(' ', '') + '/' + self.year
        save_path = self.player_name.replace(' ', '') + '/' + self.year + '/' + 'stats.csv'

        if not os.path.exists((save_dir)):
            os.mkdir(save_dir)

        if not os.path.exists(save_folder):
            os.mkdir(save_folder)

        if os.path.exists(save_path):
            os.remove(save_path)

        try:

            with open(save_path, 'w') as f:

                for cat in self.categories:
                    f.write(cat + ',')
                f.write('\n')

                for key in data_dict.keys():
                    f.write('{},'.format(data_dict[key]))
                f.write('\n')

        except IOError:
            print("I/O error")


if __name__ == '__main__':

    player_name = 'Ted Potter Jr.'
    year = '2019'

    player = GetPlayerData(year, player_name, 'WorldGolfRankings2019.csv')
    player.read_csv()
    data_dict = player.load_from_json()
    player.write_data_dict_to_csv(data_dict)
