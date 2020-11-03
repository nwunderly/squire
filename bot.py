import os
import discord
import datetime
import logging

from discord.ext import commands

from utils import settings


logger = logging.getLogger('bot')


def check(user):
    return user.id in settings.admins


class Squire(commands.Bot):
    def __init__(self, started_at, **kwargs):
        super().__init__(command_prefix=settings.prefix, **kwargs)
        self.description = "sQUIRE, Defender of Bikini Bottom"
        self.version = settings.version
        self.started_at = started_at
        self.add_check(lambda ctx: check(ctx.author))
        self.help_command = commands.MinimalHelpCommand()
        self._exit_code = 0

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}. Bot is ready.")

    async def on_message(self, message):
        # ignore bots
        if message.author.bot:
            return
        # process_commands
        else:
            await self.process_commands(message)

    def load_cogs(self):
        logger.info('Loading cogs.')
        cogs = ['jishaku'] + [f"cogs.{file[:-3]}" for file in os.listdir('./cogs') if file.endswith('.py')]
        for cog in cogs:
            try:
                self.load_extension(cog)
                logger.info(f' - {cog}')
            except commands.ExtensionFailed as e:
                logger.exception(f"Failed to load cog {cog} [{e.__class__.__name__}: {e}]")
        logger.info('Cogs loaded.')


