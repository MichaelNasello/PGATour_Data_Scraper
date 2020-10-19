import os
import requests

from bs4 import BeautifulSoup


class GolferIDS:

    def __init__(self, year, csv_path):

        self.csv_path = csv_path

        self.year = year
        self.url = 'https://www.pgatour.com/stats/stat.186.y{}.html'.format(year)

        self.player_names_with_ids = {}

        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def get_player_ids(self, num_players):

        results = self.soup.find(id='statsTable')
        for i, tr in enumerate(results.findAll('tr')):

            if not i:
                continue

            elif i == num_players:
                break

            id = tr.get('id')
            name = self.soup.find(id=id).find_all('td', class_='player-name')[0].text.replace('\n', '').replace(',', '')

            self.player_names_with_ids[name] = id.replace('playerStatsRow', '')

    def write_player_ids_to_csv(self):

        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

        try:

            with open(self.csv_path, 'w') as f:

                f.write('Player,Id\n')

                for key in self.player_names_with_ids.keys():
                    f.write('{},{}\n'.format(key, self.player_names_with_ids[key]))

        except IOError:
            print("I/O error")


if __name__ == '__main__':

    year = 2019
    rankings = GolferIDS(2019, 'WorldGolfRankings{}.csv'.format(year))

    rankings.get_player_ids(200)
    rankings.write_player_ids_to_csv()
