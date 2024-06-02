from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import utils
import json
from thorny_core import thorny_errors
import thorny_core.uikit as uikit
from thorny_core import nexus

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

    @commands.slash_command(description="See your or a user's profile")
    async def profile(self, ctx: discord.ApplicationContext,
                      user: discord.Option(discord.Member, "See someone's profile. Leave blank to see yours.",
                                           default=None)):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)

        if not thorny_guild.has_feature('profile'): raise thorny_errors.AccessDenied

        if user is None:
            user = ctx.author
        thorny_user = await nexus.ThornyUser.build(user)

        pages = [await uikit.profile_main_embed(thorny_user, thorny_guild),
                 await uikit.profile_lore_embed(thorny_user),
                 await uikit.profile_stats_embed(thorny_user)
                 ]

        await ctx.respond(embed=pages[0], view=uikit.Profile(thorny_user, pages, ctx))

    gamertag = discord.SlashCommandGroup("gamertag", "Gamertag commands")

    @gamertag.command(description="Search the database for gamertags")
    async def search(self, ctx: discord.ApplicationContext, gamertag: discord.Option(str, "Enter parts of a gamertag")):
        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")

    @commands.slash_command(description="See all upcoming birthdays!")
    async def birthdays(self, ctx: discord.ApplicationContext):
        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")
