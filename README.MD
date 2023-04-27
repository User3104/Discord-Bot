# Discord Bot

## About

This project is intended to be a simple Discord chat bot that will be capable of carrying out the following actions:

- Greeting new users that have joined the server
- Make announcements that have been rewritten by the bot owner.
- Accept commands and act based of user input
- Make announcements of upcoming at certain days before the events. (Example: one week prior, one day prior)
- Inform users of upcoming calendar events when prompted (example: `\b events`)
- More functionality may be added as needed down the line

## Implementation

The bot will be created using the `Python` programming language in order to communicate with Discord's API.
A wrapper library for Discord's API called `discord.py` will be used in conjunction with the `dotenv` package in order to speed up the programming process.

The `discord.py` package will help send our API calls to discord through HTTPS and the `dotenv` package will help to parse the .env file into variables that can be used in the program.

## Dependencies

This program wil need the followign packages to function as inteded.

```
pip install discord
pip install python-dotenv
```
