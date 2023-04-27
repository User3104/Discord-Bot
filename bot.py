from os import environ
from dotenv import load_dotenv
import discord

# read variables from .env file
load_dotenv()

# set up intents
intents = discord.Intents.default()
intents.message_content = True

# initialize client
client = discord.Client(intents=intents)


# event handler for when client is ready
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


# event handler for when a message arrives
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


# start the client
client.run(environ["DISCORD_TOKEN"])
