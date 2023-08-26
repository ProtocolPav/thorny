import discord
from discord.ext import commands

from thorny_core.db import UserFactory, commit, GuildFactory, generator


class Level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="See someone's Thorny Level, as well as their rank")
    async def level(self, ctx, user: discord.Member = None):
        thorny_guild = await GuildFactory.build(ctx.guild)
        GuildFactory.check_guild_feature(thorny_guild, 'LEVELS')

        if user is None:
            user = ctx.author
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(ctx.guild)
        last_required_xp = 100
        if thorny_user.level.level == 0:
            total_xp_to_gain = thorny_user.level.required_xp
            xp_gained = thorny_user.level.xp
        else:
            for lvl in range(1, thorny_user.level.level):
                last_required_xp += (lvl ** 2) * 4 + (50 * lvl) + 100
            total_xp_to_gain = thorny_user.level.required_xp - last_required_xp
            xp_gained = thorny_user.level.xp - last_required_xp
        percentage = round(xp_gained / total_xp_to_gain, 2)
        percentage *= 100

        rank_embed = discord.Embed(colour=user.colour)
        rank_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        if not user.is_on_mobile():
            rank_embed.set_thumbnail(url=user.display_avatar.url)
        progressbar = ""
        for i in range(int(percentage/10) if int(percentage/10) <= 10 else 10):
            progressbar = f"{progressbar}:green_square:"
        for i in range(10 - int(percentage/10)):
            progressbar = f"{progressbar}:white_large_square:"

        leaderboard, rank = await generator.levels_leaderboard(thorny_user)

        rank_embed.add_field(name=f"You are Level {thorny_user.level.level}!",
                             value=f"**Your Rank:** #{rank} on the Leaderboard\n"
                                   f"**Lv.{thorny_user.level.level}** {progressbar} "
                                   f"**Lv.{thorny_user.level.level + 1}**\n\n"
                                   f"Level {thorny_user.level.level} is {int(percentage)}% Complete")

        if not thorny_guild.levels_enabled:
            rank_embed.add_field(name="Your Level is Frozen!",
                                 value="Your server owner has disabled leveling on this server.",
                                 inline=False)

        await ctx.respond(embed=rank_embed)

    @commands.slash_command(description="Level up a user")
    @commands.has_permissions(administrator=True)
    async def levelup(self, ctx, user: discord.Member, level: int):
        thorny_guild = await GuildFactory.build(ctx.guild)
        GuildFactory.check_guild_feature(thorny_guild, 'LEVELS')

        thorny_user = await UserFactory.build(user)
        required_xp = 100
        for lvl in range(1, level):
            required_xp += (lvl ** 2) * 4 + (50 * lvl) + 100

        thorny_user.level.required_xp = required_xp
        thorny_user.level.level = level - 1
        thorny_user.level.xp = required_xp - 1
        await ctx.respond(f"{thorny_user.username} is now at Level {level}")
        await commit(thorny_user)
