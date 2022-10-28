import discord
from discord.ext import commands
from thorny_core import functions as func
import json

v = json.load(open('version.json', 'r'))['version']

home_embed = None
help_dict = {}


class Dropdown(discord.ui.View):
    options = [discord.SelectOption(label="Home", description="Go to the Thorny Help Center Home", emoji="🏡", default=True),
               discord.SelectOption(label="Configuration", description="Commands to configure Thorny", emoji="⚙️"),
               discord.SelectOption(label="Moderation", description="Commands to moderate your server", emoji="🔎"),
               discord.SelectOption(label="Money", description="Commands to do with money", emoji="💳"),
               discord.SelectOption(label="Inventory", description="Commands to do with the Inventory and Shop", emoji="🎒"),
               discord.SelectOption(label="Profile", description="Commands to do with your profile", emoji="📝"),
               discord.SelectOption(label="Playtime", description="Commands to do with playtime", emoji="⏰"),
               discord.SelectOption(label="Level", description="Commands to do with levels", emoji="🌟"),
               discord.SelectOption(label="Leaderboard", description="Leaderboards... Self explanatory", emoji="🥇")]

    @discord.ui.select(placeholder="Click on a category to see its commands",
                       min_values=1, max_values=1, options=options)
    async def callback(self, select, interaction):
        category = select.values[0]
        for item in select.options:
            if item.label == select.values[0]:
                index = select.options.index(item)
                select.options[index].default = True
            else:
                index = select.options.index(item)
                select.options[index].default = False
        if category == "Home":
            help_embed = home_embed
        else:
            help_embed = discord.Embed(title=f"{category} | Thorny Help Center",
                                       description="Click on a command to use it!",
                                       color=0x65b39b)
            text = ''
            category = category.capitalize()
            for command in help_dict[f'{category}']:
                if command['usage'] == "":
                    text = f"{text}{command['name']}\n```{command['desc']}```\n"
                else:
                    text = f"{text}{command['name']} **{command['usage']}**\n```{command['desc']}```\n"
            help_embed.set_footer(text=f"{v}")
            help_embed.add_field(name=f"**{category} Commands**",
                                 value=f"{text}")
        await interaction.response.edit_message(embed=help_embed, view=select.view)


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Access the Thorny Help Center")
    async def help(self, ctx):
        global help_dict, home_embed
        help_dict = await func.generate_help_dict(self, ctx)

        home_embed = discord.Embed(title="Home | Thorny Help Center",
                                   description="Use the **Select Menu** to see more about commands!",
                                   color=0x65b39b)
        home_embed.set_footer(text=f"{v}")
        for cog in self.client.cogs:
            easy_view_text = []

            for command in help_dict[f'{cog}']:
                easy_view_text.append(command['name'])

            if len(easy_view_text) > 3:
                easy_view_text = f"{'**,** '.join(easy_view_text[0:3])}**, `and more`**"
            elif len(easy_view_text) <= 3:
                easy_view_text = f"{'**,** '.join(easy_view_text)}"

            if cog != "Help" and easy_view_text != "":
                home_embed.add_field(name=f"**{cog} Commands**",
                                     value=f"{easy_view_text}",
                                     inline=False)

        view = Dropdown()
        for item in view.options:
            if item.label == "Home":
                index = view.options.index(item)
                view.options[index].default = True
            else:
                index = view.options.index(item)
                view.options[index].default = False
        await ctx.respond(embed=home_embed, view=view)
