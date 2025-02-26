from discord.ext import commands
import json
import thorny_errors
import uikit
import nexus
import httpx

version_file = open('./version.json', 'r+')
version = json.load(version_file)
v = version["version"]
config = json.load(open("./config.json", "r"))


class Playtime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="See connected players and how much time they've been on for")
    async def online(self, ctx):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        async with httpx.AsyncClient() as client:
            status: httpx.Response = await client.get("http://amethyst:8000/server/details", timeout=None)
            online_players = await thorny_guild.get_online_players()

        await ctx.respond(embed=uikit.server_status(online=status.json()['server_online'],
                                                    status=status.json()['server_status'],
                                                    uptime=status.json()['uptime'],
                                                    load=status.json()['usage'],
                                                    online_players=online_players,
                                                    everthorn_guilds=True))
