import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
from bs import try_load_html_as_soup

bot = commands.Bot(command_prefix='!')
hub_edgecases = {8: 12, 9: 13, 10: 14, 11: 15,
                 "g1": 11, "g2": 12, "g3": 13, "g4": 14}
high_rank_list = ["hr", "high", "h"]
low_rank_list = ["lr", "low", "l"]
g_rank_list = ["g", "g-rank"]
rank_list = high_rank_list + low_rank_list + g_rank_list
response = ""

def soupLoader(command):
    if command == "quests":
        filename = 'data/quests.html'
        URL = 'https://mhgu.kiranico.com/quest'
    if command == "items":
        filename = 'data/items.html'
        URL = 'https://mhgu.kiranico.com/item#list'
    soup = try_load_html_as_soup(filename, URL)
    return soup

def itemFinder(soup, rank, category):
    low_rank = []
    high_rank = []
    g_rank = []
    
    try:
        map_snipet = soup.find("h5",text=category)
        container = map_snipet.find_next("table")
        container = container.find_all("tr")
        for i in container:
            row = i.find_all("td")
            if len(row) > 0:
                if row[0].find(text="Low Rank"):
                    low_rank.append([x.text.strip() for x in row[1:8]])
                if row[0].find(text="High Rank"):
                    high_rank.append([x.text.strip() for x in row[1:8]])
                if row[0].find(text="G Rank"):
                    g_rank.append([x.text.strip() for x in row[1:8]])
        if rank.lower() in high_rank_list:
            return high_rank
        if rank.lower() in low_rank_list:
            return low_rank
        if rank.lower() in g_rank_list:
            return g_rank
        return low_rank + high_rank + g_rank
    
    except Exception as e:
        print(e)
        print(category.title() + " doesn't exist for this item.")

def findItemPage(item_data):
    soup = soupLoader("items")
    item_link = soup.find("a", text=item_data)
    link = item_link["href"]
    filename = "data/item_"+item_data.strip()+".html"
    soup = try_load_html_as_soup(filename, link)
    return soup

def findKeyQuests(quest_id, quest_type):
    soup = soupLoader("quests")
    if quest_type.lower() == "village":
        quest_id = "s0-"+quest_id
    if quest_type.lower() == "hub":
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

def getCommandPosition(args, search_list):
    try:
        args = list(args)
        for i,item in enumerate(args):
            if item.lower() in search_list:
                position = i
        return position

    except Exception as e:
        print(e)
        print("Error: Command  not supported!")

@bot.event
async def on_ready():
    print('{} has connected to Discord!'.format(bot.user))

@bot.command("item")
async def items(ctx, *args): 
    rank_position = getCommandPosition(args, rank_list)
    if rank_position == len(args)-1:
        item_name = " ".join(args[0:rank_position])
    else:
         item_name = " ".join(args[rank_position+1:])

    rank = args[rank_position]
    soup = findItemPage(item_name.title())

    #Get categories of item data
    itemMapData = itemFinder(soup, rank.title(), "Map")
    itemDropData = itemFinder(soup, rank.title(), "Monster")
    itemQuestData = itemFinder(soup, rank.title(), "Quest")

    if rank.lower() in high_rank_list:
        rank = "High Rank"
    if rank.lower() in low_rank_list:
        rank = "Low Rank"
    if rank.lower() in g_rank_list:
        rank = "G Rank"

    #Print
    mapMsg = item_name.title() + " [" + rank.title() + " - Map]"
    monsterMsg = item_name.title() + " [" + rank.title() + " - Monster]"
    questMsg = item_name.title() + " [" + rank.title() + " - Quest]"

    #Send out messages
    await limitMessages(ctx, itemMapData, mapMsg)
    await limitMessages(ctx, itemDropData, monsterMsg)
    if "quest".casefold() in args:
        await limitMessages(ctx, itemQuestData, questMsg)

async def limitMessages(ctx, datalist, msg):
    try:
        for data in datalist:
            msg += '\n' + ' '.join(data)
        if len(msg) >= 2000:
            msg_first = msg[:len(msg) // 2]
            msg_second = msg[len(msg) // 2:]
            await ctx.send(msg_first)
            await ctx.send(msg_second)
        else:
            await ctx.send(msg)
        await ctx.send("\n")
        
    except Exception as e:
        print(e)
        print("Error: Category does not exist for this item!")


@bot.command("key")
async def keyquest(ctx, *args):
    quest_position = getCommandPosition(args, ["hub", "village"])
    quest_type = args[quest_position]

    for i, item in enumerate(args):
        if item.isdigit():
            quest_id_position = i
            
    quest_id = args[quest_id_position]
    keyquests = findKeyQuests(quest_id, quest_type)
    await ctx.send(keyquests)

def load_token_from_file(filename):
    with open(filename, 'r') as f:
        token = f.read()
    return token

token = load_token_from_file('bot_token.txt')
bot.run(token)
