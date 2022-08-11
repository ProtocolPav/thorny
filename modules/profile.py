from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import utils
import json
from thorny_core import functions as func
from thorny_core.dbcommit import commit
from thorny_core.dbfactory import ThornyFactory

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    profile_edit_sections = ['slogan', 'gamertag', 'role', 'wiki', 'aboutme', 'lore']
    profile_edit_categories = ['activity', 'aboutme', 'lore', 'wiki']
    days = [i for i in range(1, 31)]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    years = [i for i in range(1980, 2016)]
    profile = discord.SlashCommandGroup("profile", "Different profile commands")

    @profile.command(description="See your or a player's profile")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        thorny_user = await ThornyFactory.build(user)
        await commit(thorny_user)

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.guild.roles) in user.roles:
            is_donator = f'I donated to Everthorn!\n'
        else:
            is_donator = ''

        profile_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                      color=user.color)
        profile_embed.set_author(name=user, icon_url=user.avatar.url)
        profile_embed.set_thumbnail(url=user.avatar.url)
        if thorny_user.join_date is not None:
            date_joined = datetime.strftime(thorny_user.join_date, "%B %d %Y")
        else:
            date_joined = "DM Pav to set up!"
        if thorny_user.birthday is not None:
            user_birthday = datetime.strftime(thorny_user.birthday, '%B %d %Y')
        else:
            user_birthday = "Use `/birthday` to set up!"
        profile_embed.add_field(name=f'**:card_index: Information**',
                                value=f"{is_donator}**Gamertag:** {thorny_user.profile.gamertag}\n"
                                      f"**Level:** {thorny_user.profile.level}\n"
                                      f"**Balance:** <:Nug:884320353202081833>"
                                      f"{thorny_user.balance}\n"
                                      f"**Birthday:** {user_birthday}\n"
                                      f"**Joined on:** {date_joined}")
        if thorny_user.profile.activity_shown:
            profile_embed.add_field(name=f'**:clock8: My Activity**',
                                    value=f"Use `/journal` for more stats\n**Latest Playtime:** "
                                          f"{thorny_user.playtime.recent_session}\n"
                                          f"**{datetime.now().strftime('%B')}:** "
                                          f"{thorny_user.playtime.current_playtime}\n"
                                          f"**{(datetime.now() - timedelta(days=30)).strftime('%B')}:** "
                                          f"{thorny_user.playtime.previous_playtime}\n"
                                          f"**{(datetime.now() - timedelta(days=60)).strftime('%B')}:** "
                                          f"{thorny_user.playtime.expiring_playtime}\n\n"
                                          f"**Total:** "
                                          f"{thorny_user.playtime.total_playtime}", inline=True)
        if thorny_user.profile.aboutme_shown:
            profile_embed.add_field(name=f'**:person_raising_hand: About Me**',
                                    value=f'"{thorny_user.profile.aboutme}"', inline=False)
        if thorny_user.profile.lore_shown:
            profile_embed.add_field(name=f"**:dart: My Lore**",
                                    value=f'**Role:** {thorny_user.profile.role}\n"{thorny_user.profile.lore}"',
                                    inline=False)
        if thorny_user.profile.wiki_shown and thorny_user.profile.wiki is not None:
            profile_embed.add_field(name=f'**Featured Wiki Article**',
                                    value=f"{thorny_user.profile.wiki}",
                                    inline=False)
        profile_embed.set_footer(text=f"{v} | Use /profile edit")
        await ctx.respond(embed=profile_embed)

    @profile.command(description="Edit what a section says on your profile")
    async def edit(self, ctx,
                   section: discord.Option(str, "Pick a section of your profile to edit",
                                           autocomplete=utils.basic_autocomplete(profile_edit_sections)),
                   text: discord.Option(str, "Put the text you want to appear in the section")):
        thorny_user = await ThornyFactory.build(ctx.author)
        thorny_user.profile.update(section, text)
        await commit(thorny_user)
        await Profile.view(ctx)

    @profile.command(description="Toggle visibility of a category on your profile")
    async def toggle(self, ctx,
                     category: discord.Option(str, "Pick a category to show/hide!",
                                              autocomplete=utils.basic_autocomplete(profile_edit_categories))):
        thorny_user = await ThornyFactory.build(ctx.author)
        thorny_user.profile.update(f"{category}_shown", toggle=True)
        await commit(thorny_user)
        await Profile.view(self, ctx)

    birthday = discord.SlashCommandGroup("birthday", "Birthday commands")

    @birthday.command(description="Set your birthday")
    async def set(self, ctx, month: discord.Option(str, "Pick or type a month",
                                                   autocomplete=utils.basic_autocomplete(months)),
                  day: discord.Option(int, "Pick or type a day",
                                      autocomplete=utils.basic_autocomplete(days)),
                  year: discord.Option(int, "Pick or type a year",
                                       autocomplete=utils.basic_autocomplete(years))):
        if year is not None:
            date = f'{month} {day} {year}'
            date_system = datetime.strptime(date, "%B %d %Y")
        else:
            date = f'{month} {day}'
            date_system = datetime.strptime(date, "%B %d")

        thorny_user = await ThornyFactory.build(ctx.author)
        thorny_user.birthday = date_system
        await commit(thorny_user)
        await ctx.respond(f"Your Birthday is set to: **{date}**", ephemeral=True)

    @birthday.command(description="Remove your birthday")
    async def remove(self, ctx):
        thorny_user = await ThornyFactory.build(ctx.author)
        thorny_user.birthday = None
        await commit(thorny_user)
        await ctx.respond(f"I've removed your birthday! You'll lose out on Birthday messages and gifts though :(",
                          ephemeral=True)
