from datetime import datetime, timedelta
import discord
from discord.ext import commands
import json
from functions import profile_update


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
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
        profile_embed.add_field(name=f'**:open_file_folder: Information**',
                                value=f"**Kingdom:** {kingdom.capitalize()}\n"
                                      f"**Town:** {profile[f'{ctx.author.id}']['fields']['town']}\n"
                                      f"**Role:** {profile[f'{ctx.author.id}']['fields']['role']}\n"
                                      f"**Level:** {profile[f'{ctx.author.id}']['user_level']['level']}\n"
                                      f"**Birthday:** {profile[f'{ctx.author.id}']['birthday']}\n"
                                      f"**Joined on:** {profile[f'{ctx.author.id}']['date_joined']}")
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
        profile_embed.add_field(name=f'**Featured Wiki Article**',
                                value=f"{profile[f'{ctx.author.id}']['fields']['wiki']}",
                                inline=False)
        profile_embed.add_field(name=f'**:person_raising_hand: About Me**',
                                value=f'"{profile[f"{ctx.author.id}"]["fields"]["biography"]}"',
                                inline=False)
        await ctx.send(embed=profile_embed)

    @profile.command()
    async def edit(self, ctx, field=None, *value):
        profile_update(ctx.author)
        pr_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(pr_file)

        if field is None:
            await ctx.send("Available Edits:"
                           "Slogan - Maximum 5 Words"
                           "Bio/Aboutme - Maximum 30 Words"
                           "Role - Role within kingdom"
                           "Birthday - Your Birthday!"
                           "Lore - Maximum 30 Words. About Your In-game character's lore"
                           "Wiki - Your featured wiki article")

        if field.lower() == "slogan":
            if len(value) <= 5 and len(' '.join(value)) <= 30:
                profile[str(ctx.author.id)]['fields']['slogan'] = ' '.join(value)
                await ctx.send(f'Slogan set to "{" ".join(value)}"')
            else:
                await ctx.send('Woah there buckaroo! That was more than 5 words!')

        elif field.lower() == "bio" or field.lower() == "aboutme":
            if len(value) <= 45 and len(' '.join(value)) <= 250:
                profile[str(ctx.author.id)]['fields']['biography'] = ' '.join(value)
                await ctx.send(f'Bio set to "{" ".join(value)}"')
            else:
                await ctx.send('Woah there buckaroo! That was more than 30 words!')

        elif field.lower() == "role":
            if len(value) <= 5 and len(' '.join(value)) <= 30:
                profile[str(ctx.author.id)]['fields']['role'] = ' '.join(value)
                await ctx.send(f'Role set to "{" ".join(value)}"')
            else:
                await ctx.send('Woah there buckaroo! That seems like too much for a Role')

        pr_file.truncate(0)
        pr_file.seek(0)
        json.dump(profile, pr_file, indent=3)

