import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
from bs import try_load_html_as_soup

filename = 'data/quests.html'
URL = 'https://mhgu.kiranico.com/quest'
soup = try_load_html_as_soup(filename, URL)

bot = commands.Bot(command_prefix='!')

def findKeyQuests(id, _type):
    identifier = ""
    if _type == "village":
        identifier = "s0-"+id
    if _type == "hub":
        if id == "8" or id == "9" or  id == "10" or id == "11":
            id = int(id) + 4
        elif id == "g1":
            id = 11
        elif id == "g2":
            id = 12
        elif id == "g3":
            id = 13
        elif id == "g4":
            id = 13
        identifier = "s1-"+str(id) 
    results = soup.find(id=identifier)
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

@bot.event
async def on_ready():
    print('{} has connected to Discord!'.format(bot.user))

@bot.command("key")
async def keyquest(ctx, _type, id):
    keyquests = findKeyQuests(id, _type)
    await ctx.send(keyquests)

bot.run(token)
