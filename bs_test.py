from bs4 import BeautifulSoup
from bs import try_load_html_as_soup

hub_edgecases = {8: 12, 9: 13, 10: 14, 11: 15,
                 "g1": 11, "g2": 12, "g3": 13, "g4": 14}


def soupLoader(command):
    if command == "quests":
        filename = 'data/quests.html'
        URL = 'https://mhgu.kiranico.com/quest'
    if command == "items":
        filename = 'data/items.html'
        URL = 'https://mhgu.kiranico.com/item#list'
    soup = try_load_html_as_soup(filename, URL)
    return soup


def itemFinder(soup):
    low_rank = []
    high_rank = []
    g_rank = []

    map_snipet = soup.find("h5",text="Map")
    container = map_snipet.find_next("table")
    container = container.find_all("tr")
    for i in container:
        row = i.find_all("td")
        if len(row) > 0:
            if row[0].find(text="Low Rank"):
                low_rank.append([x.text.strip() for x in row[0:8]])
            if row[0].find(text="High Rank"):
                high_rank.append([x.text.strip() for x in row[0:8]])
            if row[0].find(text="G Rank"):
                g_rank.append([x.text.strip() for x in row[0:8]])
    print(low_rank)
    print("DONE")

    print(high_rank)
    print("DONE")

    print(g_rank)
    print("DONE")


def findItemData(item_id):
    soup = soupLoader("items")
    item_link = soup.find("a", text=item_id)
    item_link = item_link["href"]
    filename = "data/item_"+item_id.strip()+".html"
    soup = try_load_html_as_soup(filename, item_link)
    itemFinder(soup)


def findKeyQuests(quest_id, quest_type):
    soup = soupLoader("quests")
    if quest_type == "village":
        quest_id = "s0-"+quest_id
    if quest_type == "hub":
        if quest_id in hub_edgecases:
            quest_id = hub_edgecases[id]
        quest_id = "s1-"+str(quest_id)
    results = soup.find(id=quest_id)
    tr_list = results.find_all('tr')
    quest_infos = []
    key_quests = []
    i = 0
    for i in range(0, len(tr_list), 2):
        quest_infos.append(tr_list[i].find_all(
            'td') + tr_list[i+1].find_all('td'))
    for quest in quest_infos:
        if quest[0].find(text='Key'):
            quest_name = quest[1].find('a').contents[0].strip()
            key_quests.append(quest_name)
    return key_quests


findItemData("Blue Mushroom")
