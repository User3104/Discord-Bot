# Discord Bot

## About

This project is intended to be a simple Discord chat bot made using Python that will be capable of carrying out the following actions:

- Greet new users
- Make announcements that have been written by the bot owner
- Accept commands and act based on user input
- Make announcements at certain time intervals before events (e.g., one week prior, one day prior)
- Inform users of upcoming calendar events when prompted (example: `/b events`)
- More functionality may be added as needed down the line

## Implementation

The bot will be created using the [Python](https://www.python.org) programming language in order to communicate with [the Discord API](https://discord.com/developers/docs). A wrapper library for Discord's API called [`discord.py`](https://discordpy.readthedocs.io) will be used in conjunction with the [`python-dotenv`](https://pypi.org/project/python-dotenv/) package in order to speed up the programming process.

The `discord.py` package will help send our API calls to discord through HTTPS, and the `python-dotenv` package will help to parse the `.env` file into variables that can be used in the program.

## Dependencies

This program will need the following packages to function as intended:

`pip install -U discord.py python-dotenv`
