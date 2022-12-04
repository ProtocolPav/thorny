import discord
from discord.ext import commands

import json
import random
from thorny_core.db import UserFactory, GuildFactory
from thorny_core.uikit import embeds


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
        if password == "pls generate":
            file = open('../thorny_data/secret_santa.json', 'r+')
            file_json: dict = json.load(file)
            list_of_people = sorted(file_json.keys())

            for key, value in file_json.items():
                who_they_got = random.choice(list_of_people)

                while who_they_got == key:
                    who_they_got = random.choice(list_of_people)

                list_of_people.pop(list_of_people.index(who_they_got))

                value['id_of_who_they_got'] = who_they_got
                file_json[who_they_got]['id_of_who_got_them'] = key

                user = await UserFactory.get(ctx.guild, int(key))
                receiver = await UserFactory.get(ctx.guild, int(who_they_got))
                await user.discord_member.send(embed=embeds.secret_santa_message(gift_receiver=receiver,
                                                                                 request=file_json[who_they_got]['request']))

            await ctx.respond("Generated Secret Santa and sent out DMs.")

            file.truncate(0)
            file.seek(0)

            json.dump(file_json, file, indent=1, default=str)
            file.close()

        else:
            await ctx.respond("Wrong password.")
