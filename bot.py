import logging
import os

import aiohttp
import disnake
from disnake.ext import commands

from utils import settings
from utils.checks import is_mod

logger = logging.getLogger("bot")
help_command = commands.MinimalHelpCommand()


class Squire(commands.Bot):
    def __init__(self, started_at, **kwargs):
        super().__init__(
            command_prefix=settings.prefix,
            description="sQUIRE, Defender of Bikini Bottom",
            help_command=help_command,
            intents=settings.intents,
            **kwargs,
        )
        self.version = settings.version
        self.started_at = started_at
        self.session = None
        self.add_check(lambda ctx: is_mod(ctx.author))
        self._exit_code = 0

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}. Bot is ready.")
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def on_message(self, message):
        # ignore bots
        if message.author.bot:
            return
        # process_commands
        else:
            await self.process_commands(message)

    def load_cogs(self):
        logger.info("Loading cogs.")
        for cog in settings.COGS:
            try:
                self.load_extension(cog)
                logger.info(f" - {cog}")
            except commands.ExtensionFailed as e:
                logger.exception(
                    f"Failed to load cog {cog} [{e.__class__.__name__}: {e}]"
                )
        logger.info("Cogs loaded.")

    async def close(self):
        await self.session.close()
        del self.session
        await super().close()
