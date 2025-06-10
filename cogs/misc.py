import asyncio
import random
import socket
import typing

import disnake
from disnake.ext import commands

from utils import settings
from utils.converters import Language
from utils.parser import ARGS
from utils.translate import Translate
from utils.utility import fetch_previous_message


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translate_api = Translate()

    @commands.command()
    async def membercount(self, ctx):
        await ctx.send(ctx.guild.member_count)

    @commands.command()
    async def joinpos(self, ctx, member: disnake.Member = None):
        member = member if member else ctx.author
        order = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        join_pos = order.index(member) + 1
        await ctx.send(join_pos)

    @commands.command()
    async def test(self, ctx):
        hostname = socket.gethostname()
        whereami = (
            "Windows"
            if ARGS.dev
            else ("Kubernetes" if "squire" in hostname else "Docker")
        )
        if random.randint(0, 1):
            await ctx.guild.me.edit(nick="Ol' Reliable")
            await ctx.send(
                f"Whoosh whoosh, on {whereami}! <:bluejellyfish:479723952265232396> v{settings.version}"
            )
        else:
            await ctx.guild.me.edit(nick="Jellyfish")
            await ctx.send(
                f"Buzz Buzz, on {whereami}! <:jellyfish:479723952890052608> v{settings.version}"
            )
        await asyncio.sleep(5)
        await ctx.guild.me.edit(nick=None)

    @commands.command(aliases=["t"])
    async def translate(
        self,
        ctx,
        lang: typing.Optional[Language] = "en",
        *,
        text: commands.clean_content = None,
    ):
        """Translates a message into a language of your choice.
        Defaults to English. If no text to translate is specified, uses the current channel's previous message."""
        if not lang:
            lang = "en"
        if not text:
            ref = ctx.message.reference
            if ref:
                if ref.cached_message:
                    text = ref.cached_message.content
            if not text:
                prev = await fetch_previous_message(ctx.message)
                text = prev.content
        translation, from_lang = await self.translate_api.translate(text, lang=lang)
        await ctx.send(f"(from {from_lang}) {translation}")


def setup(bot):
    bot.add_cog(Misc(bot))
