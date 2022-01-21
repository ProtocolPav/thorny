from datetime import datetime, timedelta
import discord
from discord.ext import commands
import json
from modules import help
import functions as func
import dbutils

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, help="See your or a player's profile")
    async def profile(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        await dbutils.simple_update('user', 'kingdom', kingdom, 'user_id', user.id)
        profile = await dbutils.Profile.select_profile(user.id)

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.message.guild.roles) in user.roles:
            is_donator = f'{user.mention} donated!\n'
        else:
            is_donator = ''

        profile_embed = discord.Embed(title=f"{profile['slogan']}",
                                      color=user.color)
        profile_embed.set_author(name=user, icon_url=user.avatar_url)
        profile_embed.set_thumbnail(url=user.avatar_url)
        if profile['information_shown']:
            date_joined = "DM Pav to set up!"
            if profile['join_date'] is not None:
                date_joined = datetime.strftime(profile['join_date'], "%B %d %Y")

            profile_embed.add_field(name=f'**:card_index: Information**',
                                    value=f"{is_donator}**Gamertag:** {profile['gamertag']}\n"
                                          f"**Kingdom:** {profile['kingdom']}\n"
                                          f"**Town:** {profile['town']}\n"
                                          f"**Level:** {profile['user_level']}\n"
                                          f"**Balance:** <:Nug:884320353202081833>"
                                          f"{profile['balance']}\n\n"
                                          f"**Birthday:** {datetime.strftime(profile['birthday'], '%B %d %Y')}\n"
                                          f"**Joined on:** {date_joined}")
            if profile['activity_shown']:
                profile_embed.add_field(name=f'**:clock8: My Activity**',
                                        value=f"Use `!journal` for more stats\n**Latest Playtime:** "
                                              f"5h34m\n"
                                              f"**{datetime.now().strftime('%B')}:** "
                                              f"4h50m\n"
                                              f"**{(datetime.now() - timedelta(days=30)).strftime('%B')}:** "
                                              f"23h55m\n"
                                              f"**{(datetime.now() - timedelta(days=60)).strftime('%B')}:** "
                                              f"12h43m\n\n"
                                              f"**Total:** "
                                              f"45h", inline=True)
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
        await ctx.send(embed=profile_embed)

    @profile.command(help="Edit what a section says on your profile. The section can be: slogan, gamertag, town, role,"
                          " birthday, wiki, aboutme or lore.",
                     usage="<section> [text...]")
    async def edit(self, ctx, section=None, *value):
        if section.lower() == "birthday":
            if len(value) == 3:
                await Profile.birthday(self, ctx, value[0], value[1], value[2])
            else:
                await Profile.birthday(self, ctx, value[0], value[1])
        else:
            update = await dbutils.Profile.update_profile(ctx.author.id, section, " ".join(value))
            if update == "length_error":
                await ctx.send("Too long of a character")
            elif update == "section_error":
                await help.Help.help(self, ctx, 'profile')
            else:
                await Profile.profile(self, ctx)

    @profile.command(help="Toggle visibility of a category on your profile. "
                          "The category can be: aboutme, activity, information, wiki or lore", usage="<category>")
    async def toggle(self, ctx, category=None):
        update = await dbutils.Profile.update_toggle(ctx.author.id, category)
        if update == "section_error":
            await help.Help.help(self, ctx, 'profile')
        else:
            await Profile.profile(self, ctx)

    @profile.command(help="See all of the sections in the profile, and how to edit them!")
    async def sections(self, ctx):
        user = ctx.author
        profile_embed = discord.Embed(title=f"5 Word Slogan - !profile edit slogan",
                                      color=user.color)
        profile_embed.set_author(name=user, icon_url=user.avatar_url)
        profile_embed.set_thumbnail(url=user.avatar_url)
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
                                      f"**{(datetime.now() - timedelta(days=30)).strftime('%B')}:** "
                                      f"23h55m\n"
                                      f"**{(datetime.now() - timedelta(days=60)).strftime('%B')}:** "
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

    @commands.command(help="Set your birthday | Format: DD Month YYYY")
    async def birthday(self, ctx, day, month, year=None):
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
        await ctx.send(f"Your Birthday is set to: **{date}**")

    @profile.command(help="CM Only | Update some sections of people's profiles", hidden=True)
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, user: discord.Member, key, *value):
        update = await dbutils.Profile.update_profile(user.id, key, " ".join(value))
        if update == "length_error":
            await ctx.send("Too long of a character")
        elif update == "section_error":
            await help.Help.help(self, ctx, 'profile')
        else:
            await ctx.send(f"{key} is now {' '.join(value)} for {user.display_name}")
