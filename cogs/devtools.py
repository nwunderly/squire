import inspect
import io
import os
from typing import Union
from urllib.parse import quote

import disnake
from disnake.ext import commands

from auth import WOLFRAM_APP_ID
from utils.converters import FetchedUser
from utils.utility import red_tick


class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def oauth(self, ctx, bot: Union[disnake.User, FetchedUser], *perms):
        """Generates an invite link for a bot with the requested perms."""
        if not bot.bot:
            await ctx.send(f"{red_tick} `{bot}` isn't a bot!")
            return
        if perms:
            p = None
            if len(perms) == 1:
                try:
                    p = disnake.Permissions(int(perms[0]))
                except ValueError:
                    pass
            if not p:
                kwargs = {}
                for perm in perms:
                    kwargs[perm] = True
                try:
                    p = disnake.Permissions(**kwargs)
                except TypeError as e:
                    await ctx.send(str(e))
                    return
        else:
            p = None
        link = disnake.utils.oauth_url(bot.id, permissions=p)
        link = "<" + link + ">"
        await ctx.send(f"Invite link for `{bot}`:\n" + link)

    @commands.command()
    async def oauthperms(self, ctx, *perms):
        """Converts permissions integer to list of permissions, and vice-versa."""
        try:
            value = int(perms[0])
            p = disnake.Permissions(value)
        except ValueError:
            p = None
            value = None
        if p:
            # int conversion worked, send list of perms
            desc = f"Permissions integer `{value}` will grant these perms: \n"
            desc += "".join([("- " + perm + "\n") for perm, val in p if val])
            return await ctx.send(desc)
        else:
            # use list of perms
            kwargs = {}
            for perm in perms:
                kwargs[perm] = True
            try:
                p = disnake.Permissions(**kwargs)
            except TypeError as e:
                return await ctx.send(e)
            desc = f"These permissions will have permissions integer `{p.value}`"
            await ctx.send(desc)

    class FindIDArgs(commands.Converter):
        async def convert(self, ctx, argument):
            if argument == "guild":
                return ctx.guild
            elif argument == "channel":
                return ctx.channel
            elif argument == "me":
                return ctx.author
            else:
                raise commands.BadArgument

    @commands.group(name="id")
    async def find_id(
        self,
        ctx,
        *,
        target: Union[
            FindIDArgs,
            disnake.TextChannel,
            disnake.VoiceChannel,
            disnake.Role,
            disnake.Member,
            disnake.User,
            disnake.PartialEmoji,
        ],
    ):
        """Attempts to convert your query to a discord object and returns its id.
        Search order: Special args, TextChannel, VoiceChannel, Role, Member, User, Emoji.
        Special args: 'guild', 'channel', 'me'"""
        await ctx.send(f"`{(type(target)).__name__}` **{target.name}**:  `{target.id}`")

    @find_id.error
    async def find_id_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send("Could not locate a snowflake based on that query.")

    # @commands.command(name="source", aliases=["src"])
    # async def get_source(self, ctx, name=None):
    #     if not name:
    #         await ctx.send("<https://github.com/nwunderly/bulbe>")
    #         return
    #     if name == "help":
    #         await ctx.send(
    #             f"<https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/help.py>"
    #         )
    #         return
    #     command = self.bot.get_command(name)
    #     cog = self.bot.get_cog(name)
    #     if command:
    #         obj = command.callback
    #     elif cog:
    #         obj = cog.__class__
    #     else:
    #         await ctx.send("I couldn't find a command or module with that name.")
    #         return
    #     path = inspect.getsourcefile(obj).replace("\\", "/")
    #     git_path = path.replace(os.getcwd().replace("\\", "/"), "", 1)
    #     git_link = "https://github.com/nwunderly/bulbe/tree/master" + git_path
    #     print(git_link)
    #     async with self.bot.session.get(git_link) as response:
    #         if response.status == 404:
    #             await ctx.send("Command or module is not yet on github.")
    #             return
    #     await ctx.send(f"<{git_link}>")

    @commands.command()
    async def wolfram(self, ctx, *, query):
        query_quoted = quote(query)
        async with self.bot.session.get(
            f"https://api.wolframalpha.com/v1/simple?appid={WOLFRAM_APP_ID}&i={query_quoted}"
        ) as resp:
            try:
                img = await resp.read()
            except Exception as e:
                await ctx.send(f"```py\n{e.__class__}: {e}\n```")

            await ctx.send(file=disnake.File(io.BytesIO(img), filename="wolfram.png"))


def setup(bot):
    bot.add_cog(DevTools(bot))
