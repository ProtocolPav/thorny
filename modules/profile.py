from datetime import datetime, timedelta
import discord
from discord.ext import commands
import json
from modules import help
from functions import profile_update
version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, help="See your or a player's profile")
    async def profile(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        else:
            pass
        kingdoms_list = ['Stregabor', 'Ambria', 'Eireann', 'Dalvasha', 'Asbahamael']
        for item in kingdoms_list:
            if discord.utils.find(lambda r: r.name == item, ctx.message.guild.roles) in user.roles:
                kingdom = item.lower()
                profile_update(user, kingdom, "kingdom")
            else:
                profile_update(user, "None", "kingdom")

        profile = json.load(open('./../thorny_data/profiles.json', 'r'))

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.message.guild.roles) in user.roles:
            is_donator = '| I am a Donator!'
        else:
            is_donator = ''

        profile_embed = discord.Embed(title=f"{profile[f'{user.id}']['fields']['slogan']} {is_donator}",
                                      color=user.color)
        profile_embed.set_author(name=user, icon_url=user.avatar_url)
        profile_embed.set_thumbnail(url=user.avatar_url)
        if profile[f'{user.id}']['is_shown']['information']:
            profile_embed.add_field(name=f'**:card_index: Information**',
                                    value=f"**Gamertag:** {profile[f'{user.id}']['fields']['gamertag']}\n"
                                          f"**Kingdom:** {profile[f'{user.id}']['kingdom'].capitalize()}\n"
                                          f"**Town:** {profile[f'{user.id}']['fields']['town']}\n"
                                          f"**Role:** {profile[f'{user.id}']['fields']['role']}\n\n"
                                          f"**Level:** {profile[f'{user.id}']['user_level']['level']}\n"
                                          f"**Balance:** <:Nug:884320353202081833>"
                                          f"{profile[f'{user.id}']['balance']}\n\n"
                                          f"**Birthday:** {profile[f'{user.id}']['birthday']['display']}\n"
                                          f"**Joined on:** {profile[f'{user.id}']['date_joined']}")
        if profile[f'{user.id}']['is_shown']['activity']:
            profile_embed.add_field(name=f'**:clock8: My Activity**',
                                    value=f"**Latest Playtime:** "
                                          f"{profile[f'{user.id}']['activity']['latest_playtime']}\n"
                                          f"**{datetime.now().strftime('%B')}:** "
                                          f"{profile[f'{user.id}']['activity']['current_month']}\n"
                                          f"**{(datetime.now()-timedelta(days=30)).strftime('%B')}:** "
                                          f"{profile[f'{user.id}']['activity']['1_month_ago']}\n"
                                          f"**{(datetime.now() - timedelta(days=60)).strftime('%B')}:** "
                                          f"{profile[f'{user.id}']['activity']['2_months_ago']}\n\n"
                                          f"**Total:** "
                                          f"{profile[f'{user.id}']['activity']['total']}h")
        if profile[f'{user.id}']['is_shown']['wiki']:
            profile_embed.add_field(name=f'**Featured Wiki Article**',
                                    value=f"{profile[f'{user.id}']['fields']['wiki']}",
                                    inline=False)
        if profile[f'{user.id}']['is_shown']['aboutme']:
            profile_embed.add_field(name=f'**:person_raising_hand: About Me**',
                                    value=f'"{profile[f"{user.id}"]["fields"]["biography"]}"',
                                    inline=False)
        if profile[f'{user.id}']['is_shown']['character_story']:
            profile_embed.add_field(name=f"**:dart: My In-Game Character's Story**",
                                    value=f'"{profile[f"{user.id}"]["fields"]["lore"]}"',
                                    inline=False)
        profile_embed.set_footer(text=f"{v} | Use !help profile for help on editing your profile!")
        await ctx.send(embed=profile_embed)

    @profile.command(help="Edit what a section says on your profile. The section can be: Slogan, Gamertag, Town, Role,"
                          " Birthday, Wiki, Aboutme or Lore.",
                     usage="<section> [text...]")
    async def edit(self, ctx, section=None, *value):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)
        wrong_field = False

        if section.lower() == "slogan":
            if len(value) <= 5 and len(" ".join(value)) <= 35:
                profile[str(ctx.author.id)]['fields']['slogan'] = " ".join(value)
            else:
                await ctx.send('Hmmmm... Seems like this was more than 5 words (35 characters)')
                wrong_field = True

        elif section.lower() == "gamertag":
            if len(" ".join(value)) <= 30:
                profile[str(ctx.author.id)]['fields']['gamertag'] = " ".join(value)
            else:
                await ctx.send('This looks like one loooong Gamertag! (over 30 characters)'
                               '\nLet Pav know if I made a mistake!')
                wrong_field = True

        elif section.lower() == "town":
            if len(" ".join(value)) <= 30:
                profile[str(ctx.author.id)]['fields']['town'] = " ".join(value)
            else:
                await ctx.send('Seems like one long name for a town! (over 30 characters)'
                               '\nLet Pav know if I made a mistake!')
                wrong_field = True

        elif section.lower() == "role":
            if len(value) <= 5 and len(" ".join(value)) <= 30:
                profile[str(ctx.author.id)]['fields']['role'] = " ".join(value)
            else:
                await ctx.send('That seems like a lot for a role! (over 30 characters)')
                wrong_field = True

        elif section.lower() == "birthday":
            await ctx.send("Ah! I actually can't change your birthday using this command just yet!\n"
                           "You should use `!birthday DD Month YYYY` to set it!")
            wrong_field = True

        elif section.lower() == "wiki":
            if 'https://everthorn.fandom.com/wiki/' in " ".join(value):
                profile[str(ctx.author.id)]['fields']['wiki'] = " ".join(value)
            else:
                await ctx.send('Woah there buckaroo! This doesnt look like no wiki link...')
                wrong_field = True

        elif section.lower() == "aboutme":
            if len(" ".join(value)) <= 250:
                profile[str(ctx.author.id)]['fields']['biography'] = " ".join(value)
            else:
                await ctx.send('This looks like it is more than 30 words! (over 250 characters)')
                wrong_field = True

        elif section.lower() == "lore":
            if len(" ".join(value)) <= 250:
                profile[str(ctx.author.id)]['fields']['lore'] = " ".join(value)
            else:
                await ctx.send('This looks like it is more than 30 words! (over 250 characters)')
                wrong_field = True

        else:
            await help.Help.help(self, ctx, 'profile')
            wrong_field = True

        if not wrong_field:
            pr_file.truncate(0)
            pr_file.seek(0)
            json.dump(profile, pr_file, indent=3)
            pr_file.close()
            await Profile.profile(self, ctx)

    @profile.command(help="Show a category on your profile. The section can be: Aboutme, Activity, Information, Wiki or"
                          " Lore", usage="<category>")
    async def show(self, ctx, category=None):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)
        wrong_field = False

        if category.lower() == "aboutme":
            profile[str(ctx.author.id)]['is_shown']['aboutme'] = True

        elif category.lower() == "activity":
            profile[str(ctx.author.id)]['is_shown']['activity'] = True

        elif category.lower() == "information" or category.lower() == "info":
            profile[str(ctx.author.id)]['is_shown']['information'] = True

        elif category.lower() == "wiki":
            profile[str(ctx.author.id)]['is_shown']['wiki'] = True

        elif category.lower() == "lore":
            profile[str(ctx.author.id)]['is_shown']['character_story'] = True

        else:
            await help.Help.help(self, ctx, 'profile')
            wrong_field = True

        if not wrong_field:
            pr_file.truncate(0)
            pr_file.seek(0)
            json.dump(profile, pr_file, indent=3)
            pr_file.close()
            await Profile.profile(self, ctx)

    @profile.command(help="Hide a category on your profile. The section can be: Aboutme, Activity, Information, Wiki or"
                          " Lore", usage="<category>")
    async def hide(self, ctx, category=None):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)
        wrong_field = False

        if category.lower() == "aboutme":
            profile[str(ctx.author.id)]['is_shown']['aboutme'] = False

        elif category.lower() == "activity":
            profile[str(ctx.author.id)]['is_shown']['activity'] = False

        elif category.lower() == "information" or category.lower() == "info":
            profile[str(ctx.author.id)]['is_shown']['information'] = False

        elif category.lower() == "wiki":
            profile[str(ctx.author.id)]['is_shown']['wiki'] = False

        elif category.lower() == "story":
            profile[str(ctx.author.id)]['is_shown']['character_story'] = False

        else:
            await help.Help.help(self, ctx, 'profile')
            wrong_field = True

        if not wrong_field:
            pr_file.truncate(0)
            pr_file.seek(0)
            json.dump(profile, pr_file, indent=3)
            pr_file.close()
            await Profile.profile(self, ctx)

    @profile.command(help="See all of the sections in the profile, and how to edit them!")
    async def sections(self, ctx):
        help_embed = discord.Embed(colour=0xCF9FFF)
        help_embed.add_field(name=":question: **Profile Help**",
                             value=f"**!profile [@player]** - View your or a player's profile\n"
                                   f"**!profile edit <field> <value>** - Edit what a certain field says on your profile"
                                   f"\n**!profile show <category>** - Show a category on your profile\n"
                                   f"**!profile hide <category>** - Hide a category on your profile")
        help_embed.add_field(name=":pencil: **Fields You Can Edit**",
                             value=f"You can edit the following fields (In order from top to bottom):\n\n"
                                   f"**Slogan** - The top part of the profile | Max. 5 words\n"
                                   f"**Gamertag** - Your Minecraft Gamertag\n"
                                   f"**Town** - The town you live in | Max. 25 characters\n"
                                   f"**Role** - Your role in your kingdom | Max. 5 words\n"
                                   f"**Birthday** - Your Birthday | Format: DD Month YYYY\n"
                                   f"**Wiki** - Featured Wiki Article | Send in the whole link!\n"
                                   f"**Aboutme** - Your Bio | Max. 30 words\n"
                                   f"**Lore** - Your In-Game Character Lore | Max. 30 words",
                             inline=False)
        help_embed.add_field(name=":lock_with_ink_pen: **Categories to Show/Hide**",
                             value=f"You can choose to show/hide the following categories:\n\n"
                                   f"**Information/Info** - General info about you\n"
                                   f"**Activity** - Your activity statistics\n"
                                   f"**Wiki** - Your featured wiki article\n"
                                   f"**Aboutme** - Your bio\n"
                                   f"**Lore** - Your In-Game Character lore",
                             inline=False)
        help_embed.set_footer(text=f"Use !help profile to see more help")
        await ctx.send(embed=help_embed)

    @commands.command(help="Set your birthday | Format: DD Month YYYY")
    async def birthday(self, ctx, day, month, year=None):
        profile_update(ctx.author)

        if year is not None:
            if 1901 < int(year) < 2020:
                date = f'{day} {month} {year}'
                date_system = datetime.strptime(date, "%d %B %Y")
            else:
                await ctx.send("Mmmmmm... That is a strange year...")
                date = 'Use !birthday DD Month YYYY'
                date_system = None
        else:
            date = f'{day} {month}'
            date_system = datetime.strptime(date, "%d %B")

        profile_update(ctx.author, f"{date}", 'birthday', 'display')
        profile_update(ctx.author, f"{date_system}", 'birthday', 'system')
        await ctx.send(f"Your Birthday is set to: **{date}**")



