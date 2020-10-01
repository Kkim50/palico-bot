import discord

client = discord.Client()

@client.event
async def on_ready():
    print('{} has connected to Discord!'.format(client.user))

client.run(token)
