import logging
import sys

import disnake
from disnake.ext import commands

logger = logging.getLogger("utils.utility")


red_tick = "<:redTick:699377558361341952>"
green_tick = "<:greenTick:699377495178346546>"
gray_tick = "<:GreyTick:652202011965521950>"
yellow_tick = "⚠"
status = {
    "online": "<:status_online:699642822378258547>",
    "idle": "<:status_idle:699642825087647784>",
    "dnd": "<:status_dnd:699642826585145397>",
    "offline": "<:status_offline:699642828309004420>",
    "streaming": "<:status_streaming:699642830842363984>",
}


def list_by_category(guild):
    channels = []
    for category, category_channels in guild.by_category():
        if category is not None:
            channels.append(category)
        for channel in category_channels:
            channels.append(channel)
    return channels


def setup_logger(name, debug, dt):
    logger = logging.getLogger(name)
    time = f"{dt.month}-{dt.day}_{dt.hour}h{dt.minute}m"

    filename = "logs/{}.log"
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    file_handler = logging.FileHandler(filename.format(time))
    # file_handler.setLevel(level)

    stream_handler = logging.StreamHandler(sys.stdout)
    # stream_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(level)
    return logger


async def fetch_previous_message(message, cache=None):
    # try cache if provided
    if cache:
        use_next = False
        for m in cache[::-1]:
            if use_next and m.channel.id == message.channel.id:
                return m
            if m.id == message.id:
                use_next = True
    # fetch if necessary
    use_next = False
    async for m in message.channel.history(limit=10):
        if use_next:
            return m
        if m.id == message.id:
            use_next = True
    return None
