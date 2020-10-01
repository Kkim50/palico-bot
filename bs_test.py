import requests
from bs4 import BeautifulSoup

url = 'https://mhgu.kiranico.com/quest'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='s0-1')
tr_list = results.find_all('tr')
print(len(tr_list))

quest_infos = []
for i in range(0, len(tr_list), 2):
    tds = tr_list[i].find_all('td') + tr_list[i + 1].find_all('td')
    quest_infos.append(tds)

print(len(quest_infos))
print(quest_infos[0])
