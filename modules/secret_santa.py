import discord
from discord.ext import commands

import json
from thorny_core.db import UserFactory, GuildFactory
from thorny_core.dbutils import User
import thorny_core.dbevent as ev


class SecretSanta(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description='Participate in Secret Santa by sending in your request!',
                            guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
    async def secretsanta(self, ctx: discord.ApplicationContext,
                          request: discord.Option(str, 'Request something specific, to help your Santa!')):
        file = open('../thorny_data/secret_santa.json', 'r+')
        file_json: dict = json.load(file)

        thorny_user = await UserFactory.build(ctx.author)

        if file_json.get(str(thorny_user.thorny_id)) is None:
            file_json[str(thorny_user.thorny_id)] = {"id_of_who_they_got": None,
                                                     "id_of_who_got_them": None,
                                                     "request": request}

        else:
            file_json[str(thorny_user.thorny_id)]['request'] = request

        await ctx.respond(file_json)

        file.truncate(0)
        file.seek(0)

        json.dump(file_json, file, indent=1, default=str)
        file.close()

    @commands.slash_command(description='CANNOT UNDO! Generate and send out Secret Santas.',
                            guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
    @commands.has_permissions(administrator=True)
    async def generatesanta(self, ctx: discord.ApplicationContext, password: str):
        ...
