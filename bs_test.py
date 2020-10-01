from bs import try_load_html_as_soup

filename = 'data/quests.html'
URL = 'https://mhgu.kiranico.com/quest'

soup = try_load_html_as_soup(filename, URL)

results = soup.find(id='s0-1')
tr_list = results.find_all('tr')
print(len(tr_list))

quest_infos = []
for i in range(0, len(tr_list), 2):
    tds = tr_list[i].find_all('td') + tr_list[i + 1].find_all('td')
    quest_infos.append(tds)

print(len(quest_infos))
print(quest_infos[0])
