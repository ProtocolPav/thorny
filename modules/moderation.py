import asyncio

import discord
from discord.ext import commands
from thorny_core.uikit.views import ProjectApplicationForm
import httpx

import json
from thorny_core.db import UserFactory, commit, GuildFactory
from thorny_core.uikit import embeds, views
from thorny_core import errors

config = json.load(open("./../thorny_data/config.json", "r"))


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

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
                          f"Check Mod Logs (<#{thorny_guild.channels.get_channel('logs')}>) for the list of deleted messages.")

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
        await ctx.defer()

        async with httpx.AsyncClient() as client:
            status = await client.post("http://thorny-bds:8000/start", timeout=None)
            if status.json()['update'] is not None:
                await ctx.respond(embed=embeds.server_update_embed(status.json()['update']))
            elif not status.json()['server_online']:
                await ctx.respond(embed=embeds.server_start_embed())
            else:
                raise errors.ServerStartStop(starting=True)

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.defer()

        async with httpx.AsyncClient() as client:
            status = await client.post("http://thorny-bds:8000/stop", timeout=None)
            if status.json()['server_online']:
                await ctx.respond(embed=embeds.server_stop_embed())
            else:
                raise errors.ServerStartStop(starting=False)

    @commands.slash_command(guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        async with httpx.AsyncClient() as client:
            r = await client.post(f"http://thorny-bds:8000/<gamertag:{thorny_user.profile.gamertag}>/kick")
            if r.json()["kicked"]:
                await ctx.respond(f"Kicked {thorny_user.profile.gamertag}")
            else:
                await ctx.respond(f"Couldn't Kick")

    whitelist = discord.SlashCommandGroup("whitelist", "Whitelist Commands")

    @whitelist.command(description="Add somebody to the server whitelist",
                       guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def add(self, ctx: discord.ApplicationContext, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        gamertags = await UserFactory.get_gamertags(thorny_user.guild_id, thorny_user.profile.gamertag)

        if not gamertags and thorny_user.profile.whitelisted_gamertag is None:
            async with httpx.AsyncClient() as client:
                r: httpx.Response = await client.get("http://thorny-bds:8000/status", timeout=None)

                if r.json()['server_online']:
                    thorny_user.profile.whitelisted_gamertag = thorny_user.profile.gamertag
                    await commit(thorny_user)

                    await client.post(f"http://thorny-bds:8000/<gamertag:{thorny_user.profile.gamertag}>/whitelist/add")

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
                r: httpx.Response = await client.get("http://thorny-bds:8000/status", timeout=None)

                if r.json()['server_online']:
                    removed_gamertag = thorny_user.profile.whitelisted_gamertag
                    thorny_user.profile.whitelisted_gamertag = None
                    await commit(thorny_user)

                    await client.post(f"http://thorny-bds:8000/<gamertag:{removed_gamertag}>/whitelist/remove")

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

        send_text = []
        for tag in gamertags:
            send_text.append(f"<@{tag['user_id']}> • {tag['whitelisted_gamertag']}")

        gamertag_embed = discord.Embed(colour=0x64d5ac)
        gamertag_embed.add_field(name=f"**Everthorn Whitelist**",
                                 value="\n".join(send_text[0:1000]))
        await ctx.respond(embed=gamertag_embed)

    @commands.slash_command(description="Send a message or set of messages to the server",
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def servermessage(self, ctx: discord.ApplicationContext, message: str, interval: int, duration: int):
        ...

    @commands.slash_command(description="Authenticate your Realm or Server in the ROA",
                            guild_ids=GuildFactory.get_guilds_by_feature('ROA'))
    async def authenticate(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.user)
        thorny_guild = await GuildFactory.build(ctx.guild)

        await ctx.respond(embed=embeds.roa_embed(),
                          view=views.ROAVerification(thorny_user, thorny_guild, ctx),
                          ephemeral=True)
