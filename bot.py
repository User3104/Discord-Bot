from os import environ
from dotenv import load_dotenv
import discord
import datetime
import random
from icalendar.cal import Calendar, Component
import datetime
from urllib import request
from threading import Timer

# read variables from .env file using the dotenv library
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

    if message.content.startswith("$events"):
        ics_file_path = r"calendar.ics"
        # Get the current date and time using the datetime library
        now = datetime.datetime.now()
        # Example of how to add days to a date
        one_week_from_now = now + datetime.timedelta(weeks=1)
        upcoming_events = [["Start", "End", "Summary"]]

        # Read the .ics file named 'calendar.ics' into a 'icalendar.Calendar' object called cal.
        with open(ics_file_path, "r") as file:
            cal = Component.from_ical(file.read())

        # Iterate over each component (event) with the name of VEVENT in the .ics file using the cal.walk() generator.
        for component in cal.walk("VEVENT"):
            event_start = component.decoded("dtstart")
            event_end = component.decoded("dtend")
            summary = component.get("summary")

            if now.date() <= event_start:
                upcoming_events.append([str(event_start), str(event_end), str(summary)])

        # Display the next three events (if any)
        NUM_OF_EVENTS = 3
        msg = "```"
        msg += "Next 3 Events (yyyy-mm-dd): \n"
        for i in range(NUM_OF_EVENTS + 1):
            msg += f"{upcoming_events[i][0]:10} - {upcoming_events[i][1]:10} - {upcoming_events[i][2]}\n"
            if i == 0:
                msg += "\n"
        msg += "```"

        await message.channel.send(msg)


# the environ package is used to pass in the environmental variable into the discord.py method
client.run(environ["DISCORD_TOKEN"])
