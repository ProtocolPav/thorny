import asyncio

import discord
from discord.ext import commands
from discord import utils
from thorny_core.uikit.views import ProjectApplicationForm
import httpx

import json
from thorny_core.db import UserFactory, commit, GuildFactory
import thorny_core.dbevent as ev
from thorny_core.dbutils import Base

config = json.load(open("./../thorny_data/config.json", "r"))


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Apply for a Project!",
                            guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
    async def apply(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=ProjectApplicationForm(ctx),
                          ephemeral=True)

    @commands.slash_command(description='CM Only | Strike someone for bad behaviour')
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

    @commands.slash_command(description='Mod Only | Purge messages')
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: discord.ApplicationContext,
                    amount: int = discord.Option(int, "The amount of messages to delete")):
        thorny_guild = await GuildFactory.build(ctx.guild)
        # Make this usable by everyone, but if a mod uses it, then it deletes messages sent by all
        # if a normal user uses this, only their messages

        messages = await ctx.channel.purge(limit=amount)
        await ctx.respond(f"Deleted {len(messages)} messages.\n"
                          f"Check Mod Logs (<#{thorny_guild.channels.logs_channel}>) for the list of deleted messages.")

    @commands.slash_command(description='CM Only | Send someone to the Gulag')
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

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
    @commands.has_permissions(administrator=True)
    async def start(self, ctx):
        await ctx.defer()
        async with httpx.AsyncClient() as client:
            r = await client.get("http://bds_webserver:8000/start", timeout=None)
            online_users = await Base.select_online(Base(), ctx.guild.id)

            if r.json()["update"]:
                await ctx.respond(f"I have found an update (version {r.json()['new_version']})!\n"
                                  f"The server has been updated and has started successfully.")

                for user in online_users:
                    thorny_user = await UserFactory.get(ctx.guild, user['thorny_user_id'])
                    connection: ev.Event = await ev.fetch(ev.DisconnectEvent, thorny_user, self.client)
                    await connection.log_event_in_database()
            elif r.json()["server_started"]:
                await ctx.respond(f"The server started successfully.")

                for user in online_users:
                    thorny_user = await UserFactory.get(ctx.guild, user['thorny_user_id'])
                    connection: ev.Event = await ev.fetch(ev.DisconnectEvent, thorny_user, self.client)
                    await connection.log_event_in_database()
            else:
                await ctx.respond(f"Could not start the server, as it is already running!")

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        async with httpx.AsyncClient() as client:
            r: httpx.Response = await client.get("http://bds_webserver:8000/stop")
            online_users = await Base.select_online(Base(), ctx.guild.id)
            for user in online_users:
                thorny_user = await UserFactory.get(ctx.guild, user['thorny_user_id'])
                connection: ev.Event = await ev.fetch(ev.DisconnectEvent, thorny_user, self.client)
                await connection.log_event_in_database()

            if r.json()["server_stopped"]:
                await ctx.respond(f"The server stopped successfully")
            else:
                await ctx.respond(f"The server is already stopped!")

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        async with httpx.AsyncClient() as client:
            r = await client.post(f"http://bds_webserver:8000/<gamertag:{thorny_user.profile.gamertag}>/kick")
            if r.json()["kicked"]:
                await ctx.respond(f"Kicked {thorny_user.profile.gamertag}")
            else:
                await ctx.respond(f"Couldn't Kick")

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
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

