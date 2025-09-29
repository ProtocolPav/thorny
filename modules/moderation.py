import discord
from discord.ext import commands
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

    @commands.slash_command(description='Start the server if it is stopped')
    @commands.has_permissions(administrator=True)
    async def start(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            status = await client.get("http://amethyst:8000/server/start", timeout=None)
            if status.json()['server_online']:
                raise thorny_errors.ServerStartStop(starting=True)
            elif status.json()['update'] is not None:
                await ctx.respond(embed=embeds.server_update_embed(status.json()['update']))
            elif not status.json()['server_online']:
                await ctx.respond(embed=embeds.server_start_embed(), ephemeral=True)

    @commands.slash_command(description='Stop the server if it is currently running')
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            status = await client.get("http://amethyst:8000/server/stop", timeout=None)
            if status.json()['server_online']:
                await ctx.respond(embed=embeds.server_stop_embed(), ephemeral=True)
            else:
                raise thorny_errors.ServerStartStop(starting=False)

    whitelist = discord.SlashCommandGroup("whitelist", "Whitelist Commands")

    @whitelist.command(description="Add somebody to the server whitelist")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx: discord.ApplicationContext, user: discord.Member):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(user)
        # gamertags = await UserFactory.get_gamertags(thorny_user.guild_id, thorny_user.profile.gamertag)
        # Gets all gamertags to ensure that this is a unique gamertag being added. Not implemented.

        if thorny_user.whitelist is None:
            async with httpx.AsyncClient() as client:
                r: httpx.Response = await client.get("http://amethyst:8000/server/details", timeout=None)

                if r.json()['server_online']:
                    thorny_user.whitelist = thorny_user.gamertag

                    await client.get(f"http://amethyst:8000/whitelist/add/{thorny_user.whitelist}")

                    await ctx.respond(f"Added {thorny_user.discord_member.mention} to the whitelist "
                                      f"under the gamertag **{thorny_user.whitelist}**")

                    await thorny_user.update()
                else:
                    raise thorny_errors.ServerNotOnline()
        # elif gamertags:
        #     raise errors.GamertagAlreadyAdded(thorny_user.profile.gamertag, gamertags[0]['user_id'])
        elif thorny_user.whitelist is not None:
            raise thorny_errors.AlreadyWhitelisted()

    @whitelist.command(description="Remove somebody from the server whitelist")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(user)

        if thorny_user.whitelist is not None:
            async with httpx.AsyncClient() as client:
                r: httpx.Response = await client.get("http://amethyst:8000/server/details", timeout=None)

                if r.json()['server_online']:
                    removed_gamertag = thorny_user.whitelist
                    thorny_user.whitelist = None

                    await client.get(f"http://amethyst:8000/whitelist/remove/{removed_gamertag}")

                    await ctx.respond(f"The gamertag **{removed_gamertag}** has been removed from the whitelist")

                    await thorny_user.update()
                else:
                    raise thorny_errors.ServerNotOnline()
        else:
            raise thorny_errors.NotWhitelisted()

    @whitelist.command(description="See the whitelist")
    @commands.has_permissions(administrator=True)
    async def view(self, ctx: discord.ApplicationContext):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")

    server_command = discord.SlashCommandGroup("send", "Minecraft BDS Commands")

    @server_command.command(description='Kick someone from the server')
    @commands.has_permissions(administrator=True)
    async def boot(self, ctx, user: discord.Member):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(user)
        async with httpx.AsyncClient() as client:
            r = await client.get(f"http://amethyst:8000/kick/{thorny_user.whitelist}")
            if r.json()["kicked"]:
                await ctx.respond(f"Kicked {thorny_user.whitelist}")
            else:
                await ctx.respond(f"Couldn't Kick")

    @server_command.command(description="Send a message or set of messages to the server")
    @commands.has_permissions(administrator=True)
    async def message(self, ctx: discord.ApplicationContext, message: str, repetitions: int):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            if repetitions != 0:
                r = await client.get(f"http://amethyst:8000/commands/message/schedule", timeout=None,
                                     params={'msg': message, 'count': repetitions})

                await ctx.respond(f"## Message Scheduled!\n**Message:** {message}\n**Repetitions:** {repetitions}")
            else:
                r = await client.get(f"http://amethyst:8000/commands/message", timeout=None,
                                     params={'msg': message})

                await ctx.respond(f"## Message Sent!\n**Message:** {message}")

    @server_command.command(description="Send an announcement to the server")
    @commands.has_permissions(administrator=True)
    async def announcement(self, ctx: discord.ApplicationContext, message: str):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            r = await client.get(f"http://amethyst:8000/commands/announce", timeout=None,
                                 params={'msg': message})

            await ctx.respond(f"## Announcement Sent!\n**Contents:** {message}")
