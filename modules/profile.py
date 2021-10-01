from datetime import datetime
import discord
from discord.ext import commands
import json
from thornyv1_3.activity import profile_update

class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def profile(self, ctx):
        profile_update(ctx.author)
        profile = json.load(open('text files/profiles.json', 'r'))
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

        profile_embed = discord.Embed(title=f"{profile[f'{ctx.author.id}']['fields']['slogan']}",
                                      color=ctx.author.color)
        profile_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        profile_embed.set_thumbnail(url=ctx.author.avatar_url)
        profile_embed.add_field(name=f'About Me:',
                                value=f"Kingdom: **{kingdom.capitalize()}**\n"
                                      f"Level: **{profile[f'{ctx.author.id}']['user_level']['level']}**")
        profile_embed.add_field(name=f'Activity:',
                                value=f"Latest Playtime: "
                                      f"**{profile[f'{ctx.author.id}']['activity']['latest_playtime']}**\n"
                                      f"{datetime.now().strftime('%B')} Playtime: "
                                      f"**{profile[f'{ctx.author.id}']['activity']['current_month']}**\n")
        profile_embed.add_field(name=f'My Bio:',
                                value=f"{profile[f'{ctx.author.id}']['fields']['biography']}",
                                inline=False)
        await ctx.send(embed=profile_embed)

    @profile.command()
    async def edit(self, ctx, field=None, *value):
        profile_update(ctx.author)
        pr_file = open('text files/profiles.json', 'r+')
        profile = json.load(pr_file)

        if field is None:
            await ctx.send("Available Edits:"
                           "Slogan - Maximum 5 Words"
                           "Bio - Maximum 30 Words"
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

        pr_file.truncate(0)
        pr_file.seek(0)
        json.dump(profile, pr_file, indent=3)

