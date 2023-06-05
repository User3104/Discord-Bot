from datetime import date, datetime
from pathlib import Path
from threading import Timer
from babel.dates import format_date, format_datetime, get_timezone
from icalendar.cal import Calendar

import requests


def append_log(log_filepath, content, overwrite=False):
    """Append `content` to `log_filepath`.

    If `overwrite` is true, replace log instead of appending."""
    mode = "w" if overwrite else "a"
    with open(log_filepath, mode, encoding="utf-8") as file:
        file.write(content)


def delete_file(filepath):
    """Delete `filepath` if it exists."""
    file = Path(filepath)
    if file.is_file():
        file.unlink()


def download_file(url, filepath):
    """Download `url` to `filepath`.

    Returns True on success, False otherwise.
    """
    try:
        # download file
        response = requests.get(url)
        if response.ok:
            # save file locally
            with open(filepath, "w", encoding="utf-8", newline="") as file:
                file.write(response.text)
                return True
        else:
            return False
    # error
    except:
        return False


def download_file_interval(url, filepath, interval, log_filepath):
    """Download `url` to `filepath` every `interval` seconds.

    Log success or failure to `log_filepath`."""
    # start thread to update file on interval
    Timer(
        interval, download_file_interval, [url, filepath, interval, log_filepath]
    ).start()

    # log whether the update succeeded or failed
    success = download_file(url, filepath)
    current_time = datetime.now().strftime("%D:%H:%M:%S")
    if success:
        output = f"{current_time}\tICS file updated\n"
    else:
        output = f"{current_time}\tError: Failed to update ICS file\n"
    append_log(log_filepath, output)


def get_next_events(
    ics_filepath,
    num_of_events=3,
    locale="en_US",
    timezone="US/Pacific",
):
    """Get the next `num_of_events` events from `ics_filepath`.

    Defaults to 3 events, US formatted date or datetime, Pacific time zone.
    """

    # get timezone object
    tzinfo = get_timezone(timezone)

    # load calendar from file
    with open(ics_filepath, "r", encoding="utf-8") as file:
        calendar = Calendar.from_ical(file.read())

    # collect future events
    events = []
    for event in calendar.walk("vevent"):
        event_start = event.decoded("dtstart")
        event_end = event.decoded("dtend")
        summary = str(event.get("summary"))

        # if event is only a date
        event_is_date_only = isinstance(event_start, date) and not isinstance(
            event_start, datetime
        )
        if event_is_date_only:
            event_is_in_future = event_start >= datetime.now(tzinfo).date()
        # if event contains a date and time
        else:
            event_is_in_future = event_start > datetime.now(tzinfo)

        # only add future events, formatted for locale and timezone
        if event_is_in_future:
            if event_is_date_only:
                start = format_date(event_start)
                end = format_date(event_end)
            else:
                start = format_datetime(event_start, locale=locale, tzinfo=tzinfo)
                end = format_datetime(event_end, locale=locale, tzinfo=tzinfo)
            events.append([start, end, summary])

        # stop upon reaching requested number of events
        if len(events) == num_of_events:
            break

    return events
