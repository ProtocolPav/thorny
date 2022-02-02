import asyncio
from datetime import datetime, timedelta
import discord
import random
from discord.ext import commands, pages
import functions as func
import errors
import json
import dbutils

v = json.load(open('version.json', 'r'))['version']


class Dropdown(discord.ui.View):
    options = [discord.SelectOption(label="Home", description="Go to the Thorny Help Center Home", emoji="🚀",
                                    default=True),
               discord.SelectOption(label="Bank", description="All Bank Commands", emoji="<:Nug:884320353202081833>"),
               discord.SelectOption(label="Leaderboard", description="All Leaderboard Commands", emoji="🔢"),
               discord.SelectOption(label="Inventory", description="All Inventory Commands", emoji="📦"),
               discord.SelectOption(label="Information", description="All Information Commands", emoji="💡"),
               discord.SelectOption(label="Profile", description="All Profile Commands", emoji="😁"),
               discord.SelectOption(label="Moderation", description="All Moderation Commands", emoji="🛡️"),
               discord.SelectOption(label="Playtime", description="All Playtime Commands", emoji="⏱️")]

    @discord.ui.select(placeholder="Click on a category to see its commands",
                       min_values=1, max_values=1, options=options)
    async def callback(self, select, interaction):
        cmd = select.values[0]
        for item in select.options:
            if item.label == select.values[0]:
                index = select.options.index(item)
                select.options[index].default = True
            else:
                index = select.options.index(item)
                select.options[index].default = False
        if cmd == "Home":
            help_embed = home_embed
        else:
            help_embed = discord.Embed(title=f"{cmd} | Thorny Help Center",
                                       description="Use `/help [command]` to see specific commands",
                                       color=0x65b39b)
            text = ''
            cmd = cmd.capitalize()
            for command in help_dict[f'{cmd}']:
                if not command['alias']:
                    text = f"{text}**/{command['name']}"
                else:
                    text = f"{text}**/{command['name']}/{'/'.join(command['alias'])}"
                if command['usage'] == "":
                    text = f"{text}**\n```{command['desc']}\nExample: {command['example']}```\n"
                else:
                    text = f"{text} {command['usage']}**\n```{command['desc']}\nExample: {command['example']}```\n"
            help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
            help_embed.add_field(name=f"**{cmd} Commands**",
                                 value=f"{text}")
        await interaction.response.edit_message(embed=help_embed, view=select.view)


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Access the Thorny Help Center")
    async def help(self, ctx, cmd: discord.Option(str, "Write a command for specific help") = None):
        global help_dict
        help_dict = await func.generate_help_dict(self, ctx)
        global home_embed

        home_embed = discord.Embed(title="Home | Thorny Help Center",
                                   description="Use `/help [command]` to see specific commands",
                                   color=0x65b39b)
        home_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
        for cog in self.client.cogs:
            easy_view_text = []
            for command in help_dict[f'{cog}']:
                easy_view_text.append(command['name'])
            if len(' '.join(easy_view_text)) >= 50:
                easy_view_text = f"/{', /'.join(easy_view_text)[0:50]}..."
            else:
                easy_view_text = f"/{', /'.join(easy_view_text)}"
            if cog != "Help":
                home_embed.add_field(name=f"**{cog} Commands**",
                                     value=f"```{easy_view_text}```",
                                     inline=False)
        if cmd is None:
            view = Dropdown()
            for item in view.options:
                if item.label == "Home":
                    index = view.options.index(item)
                    view.options[index].default = True
                else:
                    index = view.options.index(item)
                    view.options[index].default = False
            await ctx.respond(embed=home_embed, view=view)

        elif cmd.capitalize() in self.client.cogs:
            help_embed = discord.Embed(title=f"{cmd} | Thorny Help Center",
                                       description="Use `/help [command]` to see specific commands",
                                       color=0x65b39b)
            text = ''
            cmd = cmd.capitalize()
            for command in help_dict[f'{cmd}']:
                if not command['alias']:
                    text = f"{text}**/{command['name']}"
                else:
                    text = f"{text}**/{command['name']}/{'/'.join(command['alias'])}"
                if command['usage'] == "":
                    text = f"{text}**\n```{command['desc']}\nExample: {command['example']}```\n"
                else:
                    text = f"{text} {command['usage']}**\n```{command['desc']}\nExample: {command['example']}```\n"
            help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
            help_embed.add_field(name=f"**{cmd} Commands**",
                                 value=f"{text}")
            view_cog = Dropdown()
            await ctx.respond(embed=help_embed, view=view_cog)

        elif cmd == cmd.lower():
            for cog in self.client.cogs:
                for command in help_dict[f"{cog}"]:
                    if cmd == command['name'] or cmd in command['alias']:
                        text = ''
                        text2 = ''
                        if not command['alias']:
                            text = f"{text}**/{command['name']}"
                        else:
                            text = f"{text}**/{command['name']}/{'/'.join(command['alias'])}"
                        if command['usage'] == "":
                            text = f"{text}**\n```{command['desc']}\nExample: {command['example']}```\n"
                        else:
                            text = f"{text} {command['usage']}**\n```{command['desc']}\n" \
                                   f"Example: {command['example']}```\n"

                        for sim_cmd in help_dict[f"{cog}"]:
                            if command['name'][0:2] in sim_cmd['name'] and \
                                    command['name'] != sim_cmd['name']:
                                if not sim_cmd['alias']:
                                    text2 = f"{text2}**/{sim_cmd['name']}"
                                else:
                                    text2 = f"{text2}**/{sim_cmd['name']}/{'/'.join(sim_cmd['alias'])}"
                                if sim_cmd['usage'] == "":
                                    text2 = f"{text2}**\n```{sim_cmd['desc']}\nExample: {sim_cmd['example']}```\n"
                                else:
                                    text2 = f"{text2} {sim_cmd['usage']}**\n```{sim_cmd['desc']}\n" \
                                            f"Example: {sim_cmd['example']}```\n"

                        help_embed = discord.Embed(title="Thorny Help Center",
                                                   color=0x65b39b)
                        help_embed.add_field(name=f"Command Help", value=f"{text}")
                        if text2 != '':
                            help_embed.add_field(name=f"Similar Commands", value=f"{text2}",
                                                 inline=False)
                        await ctx.respond(embed=help_embed, ephemeral=True)

        else:
            await ctx.send(f"Hmm... Looks like this command doesn't exist, or you didn't Capitalize the Category!")
