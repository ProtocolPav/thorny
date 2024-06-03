import asyncio
import math
import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands, pages
from thorny_core.uikit.views import ProjectApplicationForm
import httpx

import json
from thorny_core.db import UserFactory, commit, GuildFactory, event
from thorny_core.uikit import embeds, views
from thorny_core import thorny_errors

config = json.load(open("./../thorny_data/config.json", "r"))


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.pages = []

    @commands.slash_command(description='Purge messages')
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: discord.ApplicationContext,
                    amount: int = discord.Option(int, "The amount of messages to delete")):
        messages = await ctx.channel.purge(limit=amount)
        await ctx.respond(f"Deleted {len(messages)} messages.",
                          ephemeral=True)

    @commands.slash_command(description='Send someone to the Gulag')
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

    @commands.slash_command(description='Start the server if it is stopped',
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def start(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        async with httpx.AsyncClient() as client:
            status = await client.get("http://thorny-bds:8000/server/start", timeout=None)
            if status.json()['server_online']:
                raise thorny_errors.ServerStartStop(starting=True)
            elif status.json()['update'] is not None:
                await ctx.respond(embed=embeds.server_update_embed(status.json()['update']))
            elif not status.json()['server_online']:
                await ctx.respond(embed=embeds.server_start_embed())

    @commands.slash_command(description='Stop the server if it is currently running',
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.defer()

        async with httpx.AsyncClient() as client:
            status = await client.get("http://thorny-bds:8000/server/stop", timeout=None)
            if status.json()['server_online']:
                await ctx.respond(embed=embeds.server_stop_embed())
            else:
                raise errors.ServerStartStop(starting=False)

    whitelist = discord.SlashCommandGroup("whitelist", "Whitelist Commands")

    @whitelist.command(description="Add somebody to the server whitelist",
                       guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def add(self, ctx: discord.ApplicationContext, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        gamertags = await UserFactory.get_gamertags(thorny_user.guild_id, thorny_user.profile.gamertag)

        if not gamertags and thorny_user.profile.whitelisted_gamertag is None:
            async with httpx.AsyncClient() as client:
                r: httpx.Response = await client.get("http://thorny-bds:8000/server/details", timeout=None)

                if r.json()['server_online']:
                    thorny_user.profile.whitelisted_gamertag = thorny_user.profile.gamertag
                    await commit(thorny_user)

                    await client.get(f"http://thorny-bds:8000/whitelist/add/{thorny_user.profile.gamertag}")

                    await ctx.respond(f"Added <@{thorny_user.user_id}> to the whitelist "
                                      f"under the gamertag **{thorny_user.profile.gamertag}**")
                else:
                    raise errors.ServerNotOnline()
        elif gamertags:
            raise errors.GamertagAlreadyAdded(thorny_user.profile.gamertag, gamertags[0]['user_id'])
        elif thorny_user.profile.whitelisted_gamertag is not None:
            raise errors.AlreadyWhitelisted()

    @whitelist.command(description="Remove somebody from the server whitelist",
                       guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)

        if thorny_user.profile.whitelisted_gamertag is not None:
            async with httpx.AsyncClient() as client:
                r: httpx.Response = await client.get("http://thorny-bds:8000/server/details", timeout=None)

                if r.json()['server_online']:
                    removed_gamertag = thorny_user.profile.whitelisted_gamertag
                    thorny_user.profile.whitelisted_gamertag = None
                    await commit(thorny_user)

                    await client.get(f"http://thorny-bds:8000/whitelist/remove/{removed_gamertag}")

                    await ctx.respond(f"The gamertag **{removed_gamertag}** has been removed from the whitelist")
                else:
                    raise errors.ServerNotOnline()
        else:
            raise errors.NotWhitelisted()

    @whitelist.command(description="See the whitelist",
                       guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def view(self, ctx: discord.ApplicationContext):
        gamertags = await UserFactory.get_gamertags(ctx.guild.id)

        self.pages = []

        total_pages = math.ceil(len(gamertags) / 10)
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            whitelist = []
            for tag in gamertags[start:stop]:
                whitelist.append(f"<@{tag['user_id']}> • {tag['whitelisted_gamertag']}")

            if page != total_pages + 1:
                gamertag_embed = discord.Embed(colour=0x64d5ac)
                gamertag_embed.add_field(name=f"**Everthorn Whitelist**",
                                         value="\n".join(whitelist))
                gamertag_embed.set_footer(text=f'Page {page}/{total_pages}')
                self.pages.append(gamertag_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    server_command = discord.SlashCommandGroup("send", "Minecraft BDS Commands")

    @server_command.command(description='Kick someone from the server',
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def boot(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        async with httpx.AsyncClient() as client:
            r = await client.get(f"http://thorny-bds:8000/kick/{thorny_user.profile.whitelisted_gamertag}")
            if r.json()["kicked"]:
                await ctx.respond(f"Kicked {thorny_user.profile.whitelisted_gamertag}")
            else:
                await ctx.respond(f"Couldn't Kick")

    @server_command.command(description="Send a message or set of messages to the server",
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def message(self, ctx: discord.ApplicationContext, message: str, repetitions: int):
        async with httpx.AsyncClient() as client:
            if repetitions != 0:
                r = await client.get(f"http://thorny-bds:8000/commands/message/schedule", timeout=None,
                                     params={'msg': message, 'count': repetitions})

                await ctx.respond(f"## Message Scheduled!\n**Message:** {message}\n**Repetitions:** {repetitions}")
            else:
                r = await client.get(f"http://thorny-bds:8000/commands/message", timeout=None,
                                     params={'msg': message})

                await ctx.respond(f"## Message Sent!\n**Message:** {message}")

    @server_command.command(description="Send an announcement to the server",
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def announcement(self, ctx: discord.ApplicationContext, message: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(f"http://thorny-bds:8000/commands/announce", timeout=None,
                                 params={'msg': message})

            await ctx.respond(f"## Announcement Sent!\n**Contents:** {message}")
