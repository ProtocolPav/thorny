from datetime import datetime, timedelta
import discord
from discord.ext import commands
import json
from functions import profile_update
config_file = open('../thorny_data/config.json', 'r+')
config = json.load(config_file)
v = config["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def profile(self, ctx):
        profile_update(ctx.author)
        profile = json.load(open('./../thorny_data/profiles.json', 'r'))
        kingdom = ''

        if discord.utils.find(lambda r: r.name == 'Stregabor', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'stregabor'
        elif discord.utils.find(lambda r: r.name == 'Ambria', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'ambria'
        elif discord.utils.find(lambda r: r.name == 'Eireann', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'eireann'
        elif discord.utils.find(lambda r: r.name == 'Dalvasha', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'dalvasha'
        elif discord.utils.find(lambda r: r.name == 'Asbahamael', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'asbahamael'

        if discord.utils.find(lambda r: r.name == 'Donator', ctx.message.guild.roles) in ctx.author.roles:
            is_donator = '| I am a Donator!'
        else:
            is_donator = ''

        profile_embed = discord.Embed(title=f"{profile[f'{ctx.author.id}']['fields']['slogan']} {is_donator}",
                                      color=ctx.author.color)
        profile_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        profile_embed.set_thumbnail(url=ctx.author.avatar_url)
        if profile[f'{ctx.author.id}']['is_shown']['information']:
            profile_embed.add_field(name=f'**:card_index: Information**',
                                    value=f"**Kingdom:** {kingdom.capitalize()}\n"
                                          f"**Town:** {profile[f'{ctx.author.id}']['fields']['town']}\n"
                                          f"**Role:** {profile[f'{ctx.author.id}']['fields']['role']}\n"
                                          f"**Level:** {profile[f'{ctx.author.id}']['user_level']['level']}\n"
                                          f"**Birthday:** {profile[f'{ctx.author.id}']['birthday']}\n"
                                          f"**Joined on:** {profile[f'{ctx.author.id}']['date_joined']}")
        if profile[f'{ctx.author.id}']['is_shown']['activity']:
            profile_embed.add_field(name=f'**:clock8: My Activity**',
                                    value=f"**Latest Playtime:** "
                                          f"{profile[f'{ctx.author.id}']['activity']['latest_playtime']}\n"
                                          f"**{datetime.now().strftime('%B')}:** "
                                          f"{profile[f'{ctx.author.id}']['activity']['current_month']}\n"
                                          f"**{(datetime.now()-timedelta(days=30)).strftime('%B')}:** "
                                          f"{profile[f'{ctx.author.id}']['activity']['1_month_ago']}\n"
                                          f"**{(datetime.now() - timedelta(days=60)).strftime('%B')}:** "
                                          f"{profile[f'{ctx.author.id}']['activity']['2_months_ago']}\n"
                                          f"**Total:** "
                                          f"{profile[f'{ctx.author.id}']['activity']['total']}")
        if profile[f'{ctx.author.id}']['is_shown']['wiki']:
            profile_embed.add_field(name=f'**Featured Wiki Article**',
                                    value=f"{profile[f'{ctx.author.id}']['fields']['wiki']}",
                                    inline=False)
        if profile[f'{ctx.author.id}']['is_shown']['aboutme']:
            profile_embed.add_field(name=f'**:person_raising_hand: About Me**',
                                    value=f'"{profile[f"{ctx.author.id}"]["fields"]["biography"]}"',
                                    inline=False)
        if profile[f'{ctx.author.id}']['is_shown']['character_story']:
            profile_embed.add_field(name=f"**:dart: My In-Game Character's Story**",
                                    value=f'"{profile[f"{ctx.author.id}"]["fields"]["lore"]}"',
                                    inline=False)
        profile_embed.set_footer(text=f"{v} | Use !profile edit & !profile hide/show")
        await ctx.send(embed=profile_embed)

    @profile.command()
    async def edit(self, ctx, field=None, *value):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)

        if field is None:
            await ctx.send("Available Edits:\n"
                           "Slogan - Maximum 5 Words\n"
                           "Bio/Aboutme - Maximum 30 Words\n"
                           "Role - Role within kingdom\n"
                           "Town - The Town You Live In!\n"
                           "Birthday - Your Birthday!\n"
                           "Lore - Maximum 30 Words. About Your In-game character's lore\n"
                           "Wiki - Your featured wiki article\n")

        if field.lower() == "slogan":
            if len(value) <= 5 and len(' '.join(value)) <= 30:
                profile[str(ctx.author.id)]['fields']['slogan'] = ' '.join(value)
            else:
                await ctx.send('Woah there buckaroo! That was more than 5 words!')

        elif field.lower() == "bio" or field.lower() == "aboutme":
            if len(' '.join(value)) <= 250:
                profile[str(ctx.author.id)]['fields']['biography'] = ' '.join(value)
            else:
                await ctx.send('Woah there buckaroo! That was more than 30 words!')

        elif field.lower() == "role":
            if len(value) <= 5 and len(' '.join(value)) <= 30:
                profile[str(ctx.author.id)]['fields']['role'] = ' '.join(value)
            else:
                await ctx.send('Woah there buckaroo! That seems like too much for a Role')

        elif field.lower() == "town":
            if len(' '.join(value)) <= 15:
                profile[str(ctx.author.id)]['fields']['town'] = ' '.join(value)
            else:
                await ctx.send('Woah there buckaroo! That seems like too much for a Town'
                               '\nLet Pav know if I made a mistake!')

        elif field.lower() == "lore" or field.lower() == "story":
            if len(' '.join(value)) <= 250:
                profile[str(ctx.author.id)]['fields']['lore'] = ' '.join(value)
            else:
                await ctx.send('Woah there buckaroo! That was more than 30 words!')

        elif field.lower() == "wiki" or field.lower() == "article":
            if 'https://everthorn.fandom.com/wiki/' in ' '.join(value):
                profile[str(ctx.author.id)]['fields']['wiki'] = ' '.join(value)
            else:
                await ctx.send('Woah there buckaroo! This doesnt look like no wiki link...')

        pr_file.truncate(0)
        pr_file.seek(0)
        json.dump(profile, pr_file, indent=3)
        pr_file.close()
        await Profile.profile(self, ctx)

    @profile.command()
    async def show(self, ctx, field=None):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)

        if field is None:
            await ctx.send("Available Edits:\n"
                           "Aboutme\n"
                           "Activity\n"
                           "Information\n"
                           "Lore/Story\n"
                           "Wiki\n")

        if field.lower() == "aboutme":
            profile[str(ctx.author.id)]['is_shown']['aboutme'] = True

        elif field.lower() == "bio" or field.lower() == "activity":
            profile[str(ctx.author.id)]['is_shown']['activity'] = True

        elif field.lower() == "information" or field.lower() == "info":
            profile[str(ctx.author.id)]['is_shown']['information'] = True

        elif field.lower() == "wiki":
            profile[str(ctx.author.id)]['is_shown']['wiki'] = True

        elif field.lower() == "lore" or field.lower() == "story":
            profile[str(ctx.author.id)]['is_shown']['character_story'] = True

        pr_file.truncate(0)
        pr_file.seek(0)
        json.dump(profile, pr_file, indent=3)
        pr_file.close()
        await Profile.profile(self, ctx)

    @profile.command()
    async def hide(self, ctx, field=None):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)

        if field is None:
            await ctx.send("Available Edits:\n"
                           "Aboutme\n"
                           "Activity\n"
                           "Information\n"
                           "Lore/Story\n"
                           "Wiki\n")

        if field.lower() == "aboutme":
            profile[str(ctx.author.id)]['is_shown']['aboutme'] = False

        elif field.lower() == "bio" or field.lower() == "activity":
            profile[str(ctx.author.id)]['is_shown']['activity'] = False

        elif field.lower() == "information" or field.lower() == "info":
            profile[str(ctx.author.id)]['is_shown']['information'] = False

        elif field.lower() == "wiki":
            profile[str(ctx.author.id)]['is_shown']['wiki'] = False

        elif field.lower() == "lore" or field.lower() == "story":
            profile[str(ctx.author.id)]['is_shown']['character_story'] = False

        pr_file.truncate(0)
        pr_file.seek(0)
        json.dump(profile, pr_file, indent=3)
        pr_file.close()
        await Profile.profile(self, ctx)

    @commands.command()
    async def birthday(self, ctx, day, month, year=None):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)

        if year is not None:
            if int(year) > 1820:
                date = f'{day}{month}{year}'
                date = datetime.strptime(date, "%d%B%Y")
            else:
                await ctx.send("AYO youre too old!")
                date = ''
        else:
            date = f'{day}{month}1800'
            date = datetime.strptime(date, "%d%B%Y")

        await ctx.send(date)



