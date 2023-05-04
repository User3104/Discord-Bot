from os import environ
from dotenv import load_dotenv
import discord

# read variables from .env file using the dotenv library
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
    # Does not act if the message is sent by the bot itself
    if message.author == client.user:
        return

    # If a message that has been sent starts with hello, than reply with a hello
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    # If a message that has been sent that contains the words "good job" reply with a "Thank You"
    if "good job" in message.content:
        await message.channel.send("Thank You!")


# start the client using the en
client.run(environ["DISCORD_TOKEN"])
