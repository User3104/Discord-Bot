from os import environ
from dotenv import load_dotenv
import discord
import datetime
import random
from icalendar.cal import Component
import datetime
from urllib import request
from threading import Timer


# Load environment variables from .env file using the dotenv library
load_dotenv()


# download the .ics file from the url in .env file
def download_file(url, filename):
    with request.urlopen(url) as remote_file:
        file_content = remote_file.read().decode("utf-8")
        with open(filename, "w", encoding="utf-8", newline="") as file:
            file.write(file_content)


# Update .ics calendar file every 5 min (300 seconds)
def update_file(url, filename):
    Timer(300, update_file, args=[url, filename]).start()
    download_file(url, filename)
    print("ics file updated on", datetime.datetime.now().strftime("%D:%H:%M:%S"))


update_file(environ["CALENDAR_URL"], "calendar.ics")


# set up intents
intents = discord.Intents.default()


# Define a class for the bot for use with the slash commands
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    # Sync available slash commands with Discord
    async def setup_hook(self):
        await self.tree.sync()


# initialize client
client = MyClient(intents=intents)


# event handler for when client is ready
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


# -------------------- Slash Commands --------------------


# /hello
@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Say hi!"""
    await interaction.response.send_message("Hello!")


# /date
@client.tree.command()
async def date(interaction: discord.Interaction):
    """Get the current date and time."""
    current_time = datetime.datetime.now()
    await interaction.response.send_message(f"Current date and time: {current_time}")


# / roll
@client.tree.command()
@discord.app_commands.describe(n="Number of sides on the die.")
async def roll(interaction: discord.Interaction, n: int):
    """Roll an n-sided die."""

    try:
        if n >= 100000:
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
    except (ValueError, IndexError):
        await interaction.response.send_message(
            "Please provide a valid number of sides for the die."
        )


# /events
@client.tree.command()
async def events(interaction: discord.Interaction):
    """List upcoming events."""

    ics_file_path = r"calendar.ics"
    now = datetime.datetime.now()
    upcoming_events = [["Start", "End", "Summary"]]

    with open(ics_file_path, "r") as file:
        cal = Component.from_ical(file.read())

    for component in cal.walk("VEVENT"):
        event_start = component.decoded("dtstart")
        event_end = component.decoded("dtend")
        summary = component.get("summary")

        if now.date() <= event_start:
            upcoming_events.append([str(event_start), str(event_end), str(summary)])

    NUM_OF_EVENTS = 3
    msg = "```"
    msg += "Next 3 Events (yyyy-mm-dd): \n"

    for i in range(NUM_OF_EVENTS + 1):
        msg += f"{upcoming_events[i][0]:10} - {upcoming_events[i][1]:10} - {upcoming_events[i][2]}\n"

        if i == 0:
            msg += "\n"

    msg += "```"

    await interaction.response.send_message(f"{interaction.user.mention}\n\n{msg}")


# Start the connection to Discord servers and run the bot
client.run(environ["DISCORD_TOKEN"])
