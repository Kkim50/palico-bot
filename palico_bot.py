import discord
import requests
from bs4 import BeautifulSoup

URL = 'https://mhgu.kiranico.com/quest'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='s0-1')
tr_list = results.find_all('tr')
tds = []
quest_infos = []
key_quests = []
i = 0
for i in range(0, len(tr_list), 2):
    quest_infos.append(tr_list[i].find_all('td') + tr_list[i+1].find_all('td'))
client = discord.Client()

key_quests = []
for quest in quest_infos:
    if quest[0].find(text='Key'):
        quest_name = quest[1].find('a').contents[0].strip()
        key_quests.append(quest_name)
print(key_quests)

@client.event
async def on_ready():
    print('{} has connected to Discord!'.format(client.user))

@client.event
async def on_message(message):
    if message.content.startswith('!Keyquest'):
        await message.channel.send(key_quests)

client.run(token)
