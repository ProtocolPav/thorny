import discord
from discord.ext import commands

import json
from thorny_core import errors, dbclass as db
from thorny_core.dbfactory import ThornyFactory
from thorny_core import logs
from thorny_core import functions as func
from thorny_core import dbutils
from thorny_core import dbevent as ev


class Level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def rank(self, ctx):
        thorny_user = await ThornyFactory.build(ctx.author)
        percentage = round(thorny_user.profile.xp / thorny_user.profile.required_xp, 2)
        await ctx.respond(f"You are level {thorny_user.profile.level}.\n"
                          f"You have {int(percentage*100)}% xp towards you next level.\n"
                          f"You are {thorny_user.profile.required_xp - thorny_user.profile.xp} away from next level.")