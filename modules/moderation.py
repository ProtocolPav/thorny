import asyncio

import discord
from discord.ext import commands
from datetime import datetime
from thorny_core.uikit.views import ProjectApplicationForm
import httpx

import json
from thorny_core.db import UserFactory, commit, GuildFactory
from thorny_core.dbutils import Base
from thorny_core.uikit import embeds, views

config = json.load(open("./../thorny_data/config.json", "r"))


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Apply for a Project!",
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    async def apply(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=ProjectApplicationForm(ctx),
                          ephemeral=True)

    @commands.slash_command(description='CM Only | Strike someone for bad behaviour',
                            guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    @commands.has_permissions(administrator=True)
    async def strike(self, ctx, user: discord.Member, reason):
        thorny_user = await UserFactory.build(user)
        await thorny_user.strikes.append(ctx.author.id, reason)
        strike_embed = discord.Embed(color=0xCD853F)
        strike_embed.add_field(name=f"**{user} Got Striked!**",
                               value=f"From: {ctx.author.mention}\n"
                                     f"Reason: {reason}")
        strike_embed.set_footer(text=f"Strike ID: {thorny_user.strikes.strikes[-1].strike_id}")
        await ctx.respond(embed=strike_embed)
        await commit(thorny_user)

    @commands.slash_command(description='Mod Only | Purge messages',
                            guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: discord.ApplicationContext,
                    amount: int = discord.Option(int, "The amount of messages to delete")):
        thorny_guild = await GuildFactory.build(ctx.guild)
        # Make this usable by everyone, but if a mod uses it, then it deletes messages sent by all
        # if a normal user uses this, only their messages

        messages = await ctx.channel.purge(limit=amount)
        await ctx.respond(f"Deleted {len(messages)} messages.\n"
                          f"Check Mod Logs (<#{thorny_guild.channels.logs_channel}>) for the list of deleted messages.")

    @commands.slash_command(description='CM Only | Send someone to the Gulag',
                            guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    @commands.has_permissions(administrator=True)
    async def gulag(self, ctx, user: discord.Member):
        timeout_role = discord.utils.get(ctx.guild.roles, name="Time Out")
        citizen_role = discord.utils.get(ctx.guild.roles, name="Dweller")
        not_playing_role = discord.utils.get(ctx.guild.roles, name="Dormant")
        if timeout_role not in user.roles:
            if citizen_role in user.roles:
                await user.remove_roles(citizen_role)
            elif not_playing_role in user.roles:
                await user.remove_roles(not_playing_role)
            await user.add_roles(timeout_role)
            await ctx.respond(f"{user.display_name} Has entered the Gulag! "
                              f"https://tenor.com/view/ba-sing-se-gif-20976912")
        else:
            await user.remove_roles(timeout_role)
            await user.add_roles(citizen_role)
            await ctx.respond(f"{user.display_name} Has left the Gulag! "
                              f"https://tenor.com/view/ba-sing-se-gif-20976912")

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def start(self, ctx: discord.ApplicationContext):
        thorny_guild = await GuildFactory.build(ctx.guild)
        await ctx.defer()

        async with httpx.AsyncClient() as client:
            status = await client.get("http://bds_webserver:8000/status")
            if status.json()['server_online']:
                await ctx.respond(content='The server is already running!')

            else:
                await client.post("http://bds_webserver:8000/start", timeout=None)
                await asyncio.sleep(3)

                status = await client.get("http://bds_webserver:8000/status")
                online_users = await thorny_guild.get_online_players()

                if status.json()['update'] is not None:
                    await ctx.respond(f"I have found an update (version {status.json()['update']})!\n"
                                      f"The server has been updated and has started successfully.")

                    # for user in online_users:
                    #     thorny_user = await UserFactory.get(ctx.guild, user['thorny_user_id'])
                    #
                    #     disconnection = event.Disconnect(self.client, datetime.now(), thorny_user, thorny_guild)
                    #     await disconnection.log()

                elif status.json()["server_online"]:
                    await ctx.respond(f"The server is online")

                    # for user in online_users:
                    #     thorny_user = await UserFactory.get(ctx.guild, user['thorny_user_id'])
                    #
                    #     disconnection = event.Disconnect(self.client, datetime.now(), thorny_user, thorny_guild)
                    #     await disconnection.log()

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        thorny_guild = await GuildFactory.build(ctx.guild)
        await ctx.defer()

        async with httpx.AsyncClient() as client:
            status = await client.get("http://bds_webserver:8000/status")
            if not status.json()['server_online']:
                await ctx.respond(content='The server is already stopped!')

            else:
                await client.post("http://bds_webserver:8000/stop", timeout=None)
                await asyncio.sleep(3)
                status = await client.get("http://bds_webserver:8000/status")
                online_users = await thorny_guild.get_online_players()

                # for user in online_users:
                #     thorny_user = await UserFactory.get(ctx.guild, user['thorny_user_id'])
                #
                #     disconnection = event.Disconnect(self.client, datetime.now(), thorny_user, thorny_guild)
                #     await disconnection.log()

                if not status.json()["server_online"]:
                    await ctx.respond(f"The server is offline")

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        async with httpx.AsyncClient() as client:
            r = await client.post(f"http://bds_webserver:8000/<gamertag:{thorny_user.profile.gamertag}>/kick")
            if r.json()["kicked"]:
                await ctx.respond(f"Kicked {thorny_user.profile.gamertag}")
            else:
                await ctx.respond(f"Couldn't Kick")

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        async with httpx.AsyncClient() as client:
            r = await client.post(f"http://bds_webserver:8000/<gamertag:{thorny_user.profile.gamertag}>/whitelist/add")
            if r.json()["gamertag_added"]:
                await ctx.respond(f"Whitelisted {thorny_user.profile.gamertag}")
            else:
                await ctx.respond(f"Could not whitelist {thorny_user.profile.gamertag}. "
                                  f"Either you have already whitelisted this gamertag or it does not exist.")

    @commands.slash_command(description="Authenticate your Realm or Server in the ROA",
                            guild_ids=GuildFactory.get_guilds_by_feature('ROA'))
    async def authenticate(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.guild)

        await ctx.respond(embed=embeds.roa_embed(),
                          view=views.ROAVerification(thorny_user, thorny_guild, ctx),
                          ephemeral=True)
