from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import utils
import json
from thorny_core.uikit import slashoptions, views, embeds
from thorny_core.db import UserFactory, commit

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="See your or a user's profile")
    async def profile(self, ctx: discord.ApplicationContext,
                      user: discord.Option(discord.Member, "See someone's profile. Leave blank to see yours.",
                                           default=None)):
        if user is None:
            user = ctx.author
        thorny_user = await UserFactory.build(user)

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.guild.roles) in user.roles:
            is_donator = f'I donated to Everthorn!'
        else:
            is_donator = ''

        playtime_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                            color=user.color)
        playtime_page_embed.set_footer(text=f"{v} | Playtime")

        pages = [await embeds.profile_main_embed(thorny_user, is_donator),
                 await embeds.profile_lore_embed(thorny_user),
                 await embeds.profile_stats_embed(thorny_user)]
        await ctx.respond(embed=pages[0], view=views.Profile(thorny_user, pages, ctx))

    @commands.user_command(name="Thorny Profile", description="See this user's profile")
    async def user_cmd_profile(self, ctx, member: discord.Member):
        thorny_user = await UserFactory.build(member)
        await commit(thorny_user)

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.guild.roles) in member.roles:
            is_donator = f'I donated to Everthorn!'
        else:
            is_donator = ''

        playtime_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                            color=member.color)
        playtime_page_embed.set_footer(text=f"{v} | Playtime")

        pages = [embeds.profile_main_embed(thorny_user, is_donator),
                 embeds.profile_lore_embed(thorny_user),
                 embeds.profile_stats_embed(thorny_user)]
        await ctx.respond(embed=pages[0], view=views.Profile(thorny_user, pages, ctx))

    birthday = discord.SlashCommandGroup("birthday", "Birthday commands")

    @birthday.command(description="Set your birthday")
    async def set(self, ctx, month: discord.Option(str, "Pick or type a month",
                                                   autocomplete=utils.basic_autocomplete(slashoptions.months)),
                  day: discord.Option(int, "Pick or type a day",
                                      autocomplete=utils.basic_autocomplete(slashoptions.days)),
                  year: discord.Option(int, "Pick or type a year",
                                       autocomplete=utils.basic_autocomplete(slashoptions.years))):
        if year is not None:
            date = f'{month} {day} {year}'
            date_system = datetime.strptime(date, "%B %d %Y")
        else:
            date = f'{month} {day}'
            date_system = datetime.strptime(date, "%B %d")

        thorny_user = await UserFactory.build(ctx.author)
        thorny_user.birthday.time = date_system
        await commit(thorny_user)
        await ctx.respond(f"Your Birthday is set to: **{thorny_user.birthday}**", ephemeral=True)

    @birthday.command(description="Remove your birthday")
    async def remove(self, ctx):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_user.birthday.time = None
        await commit(thorny_user)
        await ctx.respond(f"I've removed your birthday! You'll lose out on Birthday messages and gifts though :(",
                          ephemeral=True)
