from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import utils
import json
from thorny_code.modules import help
from thorny_code import functions as func
from thorny_code import dbutils
from thorny_code import dbclass as db

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    profile_edit_sections = ['slogan', 'gamertag', 'town', 'role', 'wiki', 'aboutme', 'lore']
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
        kingdom = func.get_user_kingdom(ctx, user)
        await dbutils.simple_update('user', 'kingdom', kingdom, 'user_id', user.id)
        thorny_user = await db.ThornyFactory.build(user)

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.guild.roles) in user.roles:
            is_donator = f'{user.mention} donated!\n'
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
                                      f"**Kingdom:** {thorny_user.kingdom}\n"
                                      f"**Town:** {thorny_user.profile.town}\n"
                                      f"**Level:** {thorny_user.profile.level}\n"
                                      f"**Balance:** <:Nug:884320353202081833>"
                                      f"{thorny_user.balance}\n\n"
                                      f"**Birthday:** {user_birthday}\n"
                                      f"**Joined on:** {date_joined}")
        if thorny_user.profile.activity_shown:
            profile_embed.add_field(name=f'**:clock8: My Activity**',
                                    value=f"Use `/journal` for more stats\n**Latest Playtime:** "
                                          f"Coming Soon...\n"
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
        if thorny_user.profile.wiki_shown:
            profile_embed.add_field(name=f'**Featured Wiki Article**',
                                    value=f"{thorny_user.profile.wiki}",
                                    inline=False)
        profile_embed.set_footer(text=f"{v} | Use /help profile for help on editing your profile!")
        await ctx.respond(embed=profile_embed)

    @profile.command(description="Edit what a section says on your profile")
    async def edit(self, ctx,
                   section: discord.Option(str, "Pick a section of your profile to edit",
                                           autocomplete=utils.basic_autocomplete(profile_edit_sections)),
                   value):
        thorny_user = await db.ThornyFactory.build(ctx.author)
        update = await thorny_user.profile.update(section, value)
        if update is not None:
            await ctx.respond(embed=update, ephemeral=True)
        else:
            await Profile.view(self, ctx)

    @profile.command(description="Toggle visibility of a category on your profile")
    async def toggle(self, ctx,
                     category: discord.Option(str, "Pick a category to show/hide!",
                                              autocomplete=utils.basic_autocomplete(profile_edit_categories))):
        thorny_user = await db.ThornyFactory.build(ctx.author)
        await thorny_user.profile.toggle(f"{category}_shown")
        await Profile.view(self, ctx)

    @profile.command(description="See all of the sections in the profile, and how to edit them")
    async def sections(self, ctx):
        user = ctx.author
        profile_embed = discord.Embed(title=f"This is the Slogan! Max. 35 characters",
                                      color=user.color)
        profile_embed.set_author(name=user, icon_url=user.avatar)
        profile_embed.set_thumbnail(url=user.avatar)
        profile_embed.add_field(name=f'**:card_index: Information**',
                                value=f"**Gamertag:** Your MC gamertag goes here\n"
                                      f"**Kingdom:** ||Automatic||\n"
                                      f"**Town:** Your town goes here\n"
                                      f"**Level:** ||Automatic||\n"
                                      f"**Balance:** ||Automatic||\n\n"
                                      f"**Birthday:** Use the format `Month DD YYYY`\n"
                                      f"**Joined on:** ||Automatic||")
        profile_embed.add_field(name=f'**:clock8: My Activity**',
                                value=f"All activity is automatically entered!\n"
                                      f"All you gotta do is use `/connect` and `/disconnect`!", inline=True)
        profile_embed.add_field(name=f'**:person_raising_hand: About Me**',
                                value=f'"This is your About Me section. Max. 300 characters"', inline=False)
        profile_embed.add_field(name=f"**:dart: My Lore**",
                                value=f'**Role:** You choose your role!\n'
                                      f'"And then down here, your Lore goes! Max. 300 characters"',
                                inline=False)
        profile_embed.add_field(name=f'**Featured Wiki Article**',
                                value=f"When editing this section, just paste the entire link!",
                                inline=False)
        profile_embed.add_field(name=":bangbang: **Editing Commands:**",
                                value="There's two main commands:\n"
                                      "`/profile edit` - Edit individual sections, like Slogan, Aboutme, Gamertag\n"
                                      "`/profile toggle` - Hide or show categories, like Activity, Lore, Aboutme")
        profile_embed.set_footer(text=f"{v} | Use /help profile for help on editing your profile!")
        await ctx.respond(embed=profile_embed)

    @commands.slash_command(description="Set your birthday | Format: Month DD YYYY")
    async def birthday(self, ctx, month: discord.Option(str, "Pick or type a month",
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

        thorny_user = await db.ThornyFactory.build(ctx.author)
        await thorny_user.update_birthday(date_system)
        await ctx.respond(f"Your Birthday is set to: **{date}**", ephemeral=True)

    @profile.command(description="CM Only | Update some sections of people's profiles")
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, user: discord.Member, key, *value):
        thorny_user = await db.ThornyFactory.build(user)
        if key.lower() == 'join_date':
            date = datetime.strptime(" ".join(value), '%Y-%m-%d %H:%M:%S')
            await thorny_user.join_date
            await ctx.send(f"{key} is now {' '.join(value)} for {user.display_name}")
        else:
            update = await dbutils.Profile.update_profile(user.id, key, " ".join(value))
            if update == "length_error":
                await ctx.send("Too long of a character")
            elif update == "section_error":
                await ctx.send("**Some Common Edits:**\n!profile set @player ")
            else:
                await ctx.send(f"{key} is now {' '.join(value)} for {user.display_name}")
