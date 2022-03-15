from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import utils
import json
from thorny_code.modules import help
import functions as func
from thorny_code import dbutils

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    profile = discord.SlashCommandGroup("profile", "Different profile commands")

    @profile.command(description="See your or a player's profile")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        await dbutils.simple_update('user', 'kingdom', kingdom, 'user_id', user.id)
        profile = await dbutils.Profile.select_profile(user.id)

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.guild.roles) in user.roles:
            is_donator = f'{user.mention} donated!\n'
        else:
            is_donator = ''

        profile_embed = discord.Embed(title=f"{profile['slogan']}",
                                      color=user.color)
        profile_embed.set_author(name=user, icon_url=user.avatar.url)
        profile_embed.set_thumbnail(url=user.avatar.url)
        if profile['information_shown']:
            date_joined = "DM Pav to set up!"
            if profile['join_date'] is not None:
                date_joined = datetime.strftime(profile['join_date'], "%B %d %Y")
            else:
                date_joined = "DM Pav to set up!"
            if profile['birthday'] is not None:
                birthday = datetime.strftime(profile['birthday'], '%B %d %Y')
            else:
                birthday = "Use `!birthday` to set up!"
            profile_embed.add_field(name=f'**:card_index: Information**',
                                    value=f"{is_donator}**Gamertag:** {profile['gamertag']}\n"
                                          f"**Kingdom:** {profile['kingdom']}\n"
                                          f"**Town:** {profile['town']}\n"
                                          f"**Level:** {profile['user_level']}\n"
                                          f"**Balance:** <:Nug:884320353202081833>"
                                          f"{profile['balance']}\n\n"
                                          f"**Birthday:** {birthday}\n"
                                          f"**Joined on:** {date_joined}")
            if profile['activity_shown']:
                profile_embed.add_field(name=f'**:clock8: My Activity**',
                                        value=f"Use `!journal` for more stats\n**Latest Playtime:** "
                                              f"Coming Soon...\n"
                                              f"**{datetime.now().strftime('%B')}:** "
                                              f"{profile['current_month']}\n"
                                              f"**{(datetime.now() - timedelta(days=30)).strftime('%B')}:** "
                                              f"{profile['one_month_ago']}\n"
                                              f"**{(datetime.now() - timedelta(days=60)).strftime('%B')}:** "
                                              f"{profile['two_months_ago']}\n\n"
                                              f"**Total:** "
                                              f"{profile['total_playtime']}", inline=True)
        if profile['aboutme_shown']:
            profile_embed.add_field(name=f'**:person_raising_hand: About Me**',
                                    value=f'"{profile["aboutme"]}"', inline=False)
        if profile['lore_shown']:
            profile_embed.add_field(name=f"**:dart: My Lore**",
                                    value=f'**Role:** {profile["role"]}\n"{profile["lore"]}"',
                                    inline=False)
        if profile['wiki_shown']:
            profile_embed.add_field(name=f'**Featured Wiki Article**',
                                    value=f"{profile['wiki']}",
                                    inline=False)
        profile_embed.set_footer(text=f"{v} | Use !help profile for help on editing your profile!")
        await ctx.respond(embed=profile_embed)

    @view.error
    async def view_error(self, ctx, error):
        if isinstance(error, discord.ApplicationCommandInvokeError):
            await ctx.respond("You're on cooldown! Please wait a bit before using!")

    @staticmethod
    async def get_sections(ctx):
        sections = ['slogan', 'gamertag', 'town', 'role', 'wiki', 'aboutme', 'lore']
        return sections

    @profile.command(description="Edit what a section says on your profile")
    async def edit(self, ctx, section: discord.Option(str, "Pick a section to edit!",
                                                      autocomplete=utils.basic_autocomplete(get_sections)), value):
        update = await dbutils.Profile.update_profile(ctx.author.id, section, value)
        if update == "length_error":
            await ctx.send("This message is too long! Try shortening it please!")
        elif update == "section_error":
            await help.Help.help(self, ctx, 'profile')
        else:
            await Profile.view(self, ctx)

    @staticmethod
    async def get_categories(ctx):
        sections = ['information', 'activity', 'aboutme', 'lore', 'wiki']
        return sections

    @profile.command(description="Toggle visibility of a category on your profile")
    async def toggle(self, ctx, category: discord.Option(str, "Pick a category to show/hide!",
                                                         autocomplete=utils.basic_autocomplete(get_categories))):
        update = await dbutils.Profile.update_toggle(ctx.author.id, category)
        if update == "section_error":
            await help.Help.help(self, ctx, 'profile')
        else:
            await Profile.view(self, ctx)

    @profile.command(description="See all of the sections in the profile, and how to edit them")
    async def sections(self, ctx):
        user = ctx.author
        profile_embed = discord.Embed(title=f"5 Word Slogan - !profile edit slogan",
                                      color=user.color)
        profile_embed.set_author(name=user, icon_url=user.avatar)
        profile_embed.set_thumbnail(url=user.avatar)
        profile_embed.add_field(name=f'**:card_index: Information\n!profile toggle information**',
                                value=f"`!profile edit gamertag:` ProvenSpire54\n"
                                      f"**Kingdom:** Automatic\n"
                                      f"`!profile edit town:` Pastiria\n"
                                      f"**Level:** Automatic\n"
                                      f"**Balance:** Automatic\n\n"
                                      f"`!birthday:` DD Month YYYY\n"
                                      f"**Joined on:** Automatic")
        profile_embed.add_field(name=f'**:clock8: My Activity\n!profile toggle activity**',
                                value=f"Use `!journal` for more stats\n**Latest Playtime:** "
                                      f"5h34m\n"
                                      f"**{datetime.now().strftime('%B')}:** "
                                      f"4h50m\n"
                                      f"**{(datetime.now().replace(month=-1)).strftime('%B')}:** "
                                      f"23h55m\n"
                                      f"**{(datetime.now().replace(month=-2)).strftime('%B')}:** "
                                      f"12h43m\n\n"
                                      f"**Total:** "
                                      f"3 days, 4h50m", inline=True)
        profile_embed.add_field(name=f'**:person_raising_hand: About Me\n!profile toggle aboutme**',
                                value=f'`!profile edit aboutme`', inline=False)
        profile_embed.add_field(name=f"**:dart: My Lore\n!profile toggle lore**",
                                value=f'`!profile edit role:` Local Peasant\n`!profile edit lore`',
                                inline=False)
        profile_embed.add_field(name=f'**Featured Wiki Article\n!profile toggle wiki**',
                                value=f"`!profile edit wiki`",
                                inline=False)
        profile_embed.set_footer(text=f"{v} | Use !help profile for help on editing your profile!")
        await ctx.send(embed=profile_embed)

    @staticmethod
    async def get_months(ctx):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        return months

    @commands.slash_command(description="Set your birthday | Format: DD Month YYYY")
    async def birthday(self, ctx, day, month: discord.Option(str, autocomplete=utils.basic_autocomplete(get_months)),
                       year=None):
        if year is not None:
            if 1901 < int(year) < 2015:
                date = f'{month} {day} {year}'
                date_system = datetime.strptime(date, "%B %d %Y")
            else:
                await ctx.send("Mmmmmm... That is a strange year...")
                date = 'Use !birthday DD Month YYYY'
                date_system = None
        else:
            date = f'{month} {day}'
            date_system = datetime.strptime(date, "%B %d")

        await dbutils.simple_update('user', 'birthday', date_system, 'user_id', ctx.author.id)
        await ctx.respond(f"Your Birthday is set to: **{date}**", ephemeral=True)

    @profile.command(description="CM Only | Update some sections of people's profiles")
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, user: discord.Member, key, *value):
        if key.lower() == 'join_date':
            date = datetime.strptime(" ".join(value), '%Y-%m-%d %H:%M:%S')
            await dbutils.simple_update('user', 'join_date', date, 'user_id', user.id)
            await ctx.send(f"{key} is now {' '.join(value)} for {user.display_name}")
        else:
            update = await dbutils.Profile.update_profile(user.id, key, " ".join(value))
            if update == "length_error":
                await ctx.send("Too long of a character")
            elif update == "section_error":
                await ctx.send("**Some Common Edits:**\n!profile set @player ")
            else:
                await ctx.send(f"{key} is now {' '.join(value)} for {user.display_name}")
