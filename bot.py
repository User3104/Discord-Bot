from os import environ
from dotenv import load_dotenv
import discord
import datetime
import random


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

    if message.content.startswith("$date") or message.content.startswith("$time"):
        current_time = datetime.datetime.now()
        await message.channel.send(f"Current date and time: {current_time}")

    if message.content.startswith("$roll"):
        try:
            sides = int(message.content.split()[1])
            if sides >= 100000:
                await message.channel.send(f"Sorry, that is too many sides.")
            elif sides < 2:
                await message.channel.send(f"A die needs to have at least two sides.")
            else:
                result = random.randint(1, sides)
                await message.channel.send(f"🎲 A {sides} sided die landed on {result}.")
        except (ValueError, IndexError):
            await message.channel.send(
                f"Please provide a valid number of sides for the die."
            )


# start the client using the dotenv package
client.run(environ["DISCORD_TOKEN"])
