import discord
from discord.ext import commands

import json
from thorny_core.db import UserFactory
from thorny_core.dbutils import User
import thorny_core.dbevent as ev


class SecretSanta(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def secretsanta(self, ctx: discord.ApplicationContext,
                          request: discord.Option(str, 'Request something specific, to help your Santa!')):
        file = open("../secret_santa.json", "a")
        file_json = json.load(file)

        await ctx.respond(file_json)

        file.close()
