import math

import discord
from discord.ext import commands, pages
import httpx

import json
from uikit import embeds
import nexus, thorny_errors


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

    whitelist = discord.SlashCommandGroup("whitelist", "Whitelist Commands")

    @whitelist.command(description="Add somebody to the server whitelist")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx: discord.ApplicationContext, user: discord.Member):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(user)
        # gamertags = await UserFactory.get_gamertags(thorny_user.guild_id, thorny_user.profile.gamertag)
        # Gets all gamertags to ensure that this is a unique gamertag being added. Not implemented.

        if thorny_user.whitelist is None and thorny_user.gamertag is not None:
            thorny_user.whitelist = thorny_user.gamertag

            await ctx.respond(f"Added {thorny_user.discord_member.mention} to the whitelist "
                              f"under the gamertag **{thorny_user.whitelist}**")

            await thorny_user.update()
        # elif gamertags:
        #     raise errors.GamertagAlreadyAdded(thorny_user.profile.gamertag, gamertags[0]['user_id'])
        elif thorny_user.whitelist is not None:
            raise thorny_errors.AlreadyWhitelisted()
        elif thorny_user.gamertag is None:
            raise thorny_errors.NoGamertag()

    @whitelist.command(description="Remove somebody from the server whitelist")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(user)

        if thorny_user.whitelist is not None:
            removed_gamertag = thorny_user.whitelist
            thorny_user.whitelist = None

            await ctx.respond(f"Removed {thorny_user.discord_member.mention} from the whitelist "
                              f"(Removed gamertag: **{removed_gamertag}**)")

            await thorny_user.update()
        else:
            raise thorny_errors.NotWhitelisted()

    @whitelist.command(description="See the whitelist")
    async def view(self, ctx: discord.ApplicationContext):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        await ctx.defer()
        all_pages = []
        whitelisted_users: list[nexus.ThornyUser] = []

        for member in ctx.guild.members:
            if not member.bot:
                thorny_user = await nexus.ThornyUser.build(member)
                if thorny_user.whitelist:
                    whitelisted_users.append(thorny_user)

        whitelisted_users.sort(key=lambda x: x.whitelist)

        total_pages = math.ceil(len(whitelisted_users) / 10)
        all_texts = []
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            whitelist_text = []
            for user in whitelisted_users[start:stop]:
                whitelist_text.append(f'{user.discord_member.mention} • **{user.whitelist}**')

            if page != total_pages + 1:
                all_texts.append(whitelist_text)

        for text in all_texts:
            lb_embed = discord.Embed(title=f'**Everthorn Whitelist**',
                                     description='Check the guidelines to get whitelisted!',
                                     color=0x8DA5E0)
            lb_embed.add_field(name=f'',
                               value='\n'.join(text), inline=False)
            lb_embed.set_footer(text=f'Page {all_texts.index(text) + 1}/{total_pages}')
            all_pages.append(lb_embed)

        if not all_pages:
            raise thorny_errors.UnexpectedError2("No whitelist data")

        paginator = pages.Paginator(pages=all_pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    server_command = discord.SlashCommandGroup("geode", "Control the Geode server")

    @server_command.command(description='Start the server if it is stopped')
    @commands.has_permissions(administrator=True)
    async def start(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            status = await client.post("http://geode:8000/controls/start", timeout=None)
            if status.status_code == 201:
                await ctx.respond(embed=embeds.server_start_embed(), ephemeral=True)
            else:
                raise thorny_errors.ServerStartStop(starting=True)

    @server_command.command(description='Stop the server if it is currently running')
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            status = await client.post("http://geode:8000/controls/stop", timeout=None)
            if status.status_code == 201:
                await ctx.respond(embed=embeds.server_stop_embed(), ephemeral=True)
            else:
                raise thorny_errors.ServerStartStop(starting=False)

    @server_command.command(description='Restart the server if it is currently running')
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            status = await client.post("http://geode:8000/controls/restart", timeout=None)
            if status.status_code == 201:
                await ctx.respond(embed=embeds.server_stop_embed(), ephemeral=True)
            else:
                raise thorny_errors.ServerStartStop(starting=False)

    @server_command.command(description='Kick someone from the server')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(user)
        async with httpx.AsyncClient() as client:
            r = await client.post(f"http://geode:8000/controls/command", json={"command": f'kick "{thorny_user.whitelist}"'})
            if r.status_code == 201:
                await ctx.respond(f"Kicked {thorny_user.whitelist}")
            else:
                await ctx.respond(f"Couldn't Kick")

    @server_command.command(description="Send a message or set of messages to the server")
    @commands.has_permissions(administrator=True)
    async def message(self, ctx: discord.ApplicationContext, message: str, repetitions: int, interval_hours: int = 2):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            r = await client.post(f"http://geode:8000/messages/schedule", timeout=None,
                                  json={
                                      "content": message,
                                      "type": 'message',
                                      "repetitions": repetitions,
                                      "interval_seconds": interval_hours * 60 * 60
                                  })

            await ctx.respond(f"## Message Scheduled!\n**Message:** {message}\n**Repetitions:** {repetitions}")

    @server_command.command(description="Send an announcement to the server")
    @commands.has_permissions(administrator=True)
    async def announcement(self, ctx: discord.ApplicationContext, message: str):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            r = await client.post(f"http://geode:8000/messages/schedule", timeout=None,
                                  json={
                                      "content": message,
                                      "type": 'announcement',
                                      "repetitions": 1,
                                      "interval_seconds": 1
                                  })

            await ctx.respond(f"## Announcement Scheduled!\n**Message:** {message}\n")
