import random
from datetime import datetime
from os import environ

import discord
import requests
from dotenv import load_dotenv
from babel.dates import format_datetime, get_timezone

import bot
import utils

# load environment variables from .env file
load_dotenv()

# secret API key used to authenticate the bot
DISCORD_TOKEN = environ["DISCORD_TOKEN"]

# direct link to iCalendar file
CALENDAR_URL = environ["CALENDAR_URL"]

# local filepath where calendar will be saved
CALENDAR_FILEPATH = environ["CALENDAR_FILEPATH"]

# time interval (in seconds) for the bot to download the ICS file and make announcements as needed
UPDATE_INTERVAL = int(environ["UPDATE_INTERVAL"])

# log file
LOG_FILEPATH = environ["LOG_FILEPATH"]


# initialize Discord client for bot
client = bot.DiscordClient()


# event handler for when client is ready
@client.event
async def on_ready():
    print(f"Bot logged in successfully as {client.user}")

    # delete log file
    utils.delete_file(LOG_FILEPATH)

    # update the calendar file regularly
    utils.download_file_interval(
        CALENDAR_URL, CALENDAR_FILEPATH, UPDATE_INTERVAL, LOG_FILEPATH
    )


# /hello
@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Say hi!"""
    msg = f"{interaction.user.mention} Hello! 👋"
    await interaction.response.send_message(msg)


# /date
@client.tree.command()
async def date(interaction: discord.Interaction):
    """Get the current date and time."""
    now = datetime.now(get_timezone("US/Pacific"))
    now = format_datetime(now, locale="en_US")
    msg = f"Current date and time (Pacific time zone)\n{now}"
    await interaction.response.send_message(msg)


# /flip
@client.tree.command()
async def flip(interaction: discord.Interaction):
    """Flip a coin."""
    side = random.choice(["heads", "tails"])
    await interaction.response.send_message("A coin lands on " + side + ".")


# /cat
@client.tree.command()
async def cat(interaction: discord.Interaction):
    """Fetch a random cat GIF."""
    cat_api_url = "https://api.thecatapi.com/v1/images/search?mime_types=GIF"
    gif_url = requests.get(cat_api_url).json()[0]["url"]
    await interaction.response.send_message(gif_url)


# /map
@client.tree.command()
async def map(interaction: discord.Interaction):
    """Random EB map."""

    with open("maps.txt", "r") as file:
        maps = [line.strip() for line in file.readlines()]

    choice = random.choice(maps)
    await interaction.response.send_message("Random EB map: " + choice + ".")


# /faction
@client.tree.command()
async def faction(interaction: discord.Interaction):
    """Random EB Faction."""

    with open("factions.txt", "r") as file:
        factions = [line.strip() for line in file.readlines()]

    choice = random.choice(factions)
    await interaction.response.send_message("Random EB faction: " + choice + ".")


# /roll
@client.tree.command()
@discord.app_commands.describe(n="Number of sides on the die (2 to 100000).")
async def roll(interaction: discord.Interaction, n: int = 6):
    """Roll an n-sided die (default: 6)."""

    try:
        if n > 100000:
            await interaction.response.send_message("Sorry, that is too many sides.")
        elif n < 2:
            await interaction.response.send_message(
                "A die needs to have at least two sides."
            )
        else:
            result = random.randint(1, n)
            await interaction.response.send_message(
                f"🎲 A {n}-sided die landed on {result}."
            )
    except:
        await interaction.response.send_message(
            "Please provide a valid number of sides for the die."
        )


# /events
@client.tree.command()
async def events(
    interaction: discord.Interaction,
):
    """List upcoming events.

    Defaults to 3 events, US formatted datetime, Pacific time zone.
    """
    events = utils.get_next_events(CALENDAR_FILEPATH)
    num_of_events = len(events)
    if num_of_events == 0:
        return await interaction.response.send_message("No upcoming events.")

    # construct message
    width = 28
    msg = f"Next {num_of_events} events (Pacific time zone):\n```"
    msg += f"{'Start':{width}}{'End':{width}}Summary\n"
    for event in events:
        start, end, summary = event
        msg += f"{start:{width}}{end:{width}}{summary}\n"
    msg += "```"

    await interaction.response.send_message(msg)


# start the bot
client.run(DISCORD_TOKEN)
