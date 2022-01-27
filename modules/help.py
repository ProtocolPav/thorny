from datetime import datetime, timedelta
import discord
import random
from discord.ext import commands
import errors
import json

v = json.load(open('version.json', 'r'))['version']


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['hlp'], invoke_without_command=True, help="Access the Thorny Help Center")
    async def help(self, ctx, cmd=None):
        help_dict = {}
        for cog in self.client.cogs:
            help_dict[f"{cog}"] = []
            cmd_num = 0
            for command in self.client.get_cog(cog).get_commands():
                cmd_num += 1
                if not command.hidden:
                    help_dict[f"{cog}"].append({"name": command.name, "usage": command.signature,
                                                "alias": command.aliases, "desc": command.help,
                                                "example": command.brief})
                elif command.hidden and ctx.author.guild_permissions.administrator:
                    help_dict[f"{cog}"].append({"name": command.name, "usage": command.signature,
                                                "alias": command.aliases, "desc": command.help,
                                                "example": command.brief})
                if isinstance(command, commands.Group):
                    for subcommand in command.walk_commands():
                        cmd_num += 1
                        if not subcommand.hidden:
                            help_dict[f"{cog}"].append({"name": f"{command.name} {subcommand.name}",
                                                        "usage": subcommand.signature,
                                                        "alias": subcommand.aliases, "desc": subcommand.help,
                                                        "example": subcommand.brief})
                        elif subcommand.hidden and ctx.author.guild_permissions.administrator:
                            help_dict[f"{cog}"].append({"name": f"{command.name} {subcommand.name}",
                                                        "usage": subcommand.signature,
                                                        "alias": subcommand.aliases, "desc": subcommand.help,
                                                        "example": subcommand.brief})
        if cmd is None:
            help_embed = discord.Embed(title="Thorny Help Center",
                                       description="Use `!help [command]` to see specific commands\n"
                                                   "Use `!help [Category]` to see specific categories! (Capitalize)",
                                       color=0x65b39b)
            help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
            for cog in self.client.cogs:
                easy_view_text = []
                for command in help_dict[f'{cog}']:
                    easy_view_text.append(command['name'])
                if len(' '.join(easy_view_text)) >= 50:
                    easy_view_text = f"!{', !'.join(easy_view_text)[0:50]}..."
                else:
                    easy_view_text = f"!{', !'.join(easy_view_text)}"
                help_embed.add_field(name=f"**{cog} Commands**",
                                     value=f"```{easy_view_text}```",
                                     inline=False)
            await ctx.send(embed=help_embed)

        elif cmd.capitalize() in self.client.cogs:
            help_embed = discord.Embed(title="Thorny Help Center",
                                       description="Use `!help [command]` to see specific commands\n"
                                                   "Do not include brackets in commands, they just show the"
                                                   " `[optional]` and `<required>` fields of a command",
                                       color=0x65b39b)
            text = ''
            cmd = cmd.capitalize()
            for command in help_dict[f'{cmd}']:
                if not command['alias']:
                    text = f"{text}**!{command['name']}"
                else:
                    text = f"{text}**!{command['name']}/{'/'.join(command['alias'])}"
                if command['usage'] == "":
                    text = f"{text}**\n```{command['desc']}\nExample: {command['example']}```\n"
                else:
                    text = f"{text} {command['usage']}**\n```{command['desc']}\nExample: {command['example']}```\n"
            help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
            help_embed.add_field(name=f"**{cmd} Commands**",
                                 value=f"{text}")
            await ctx.send(embed=help_embed)

        elif cmd == cmd.lower():
            for cog in self.client.cogs:
                for command in help_dict[f"{cog}"]:
                    if cmd == command['name'] or cmd in command['alias']:
                        text = ''
                        text2 = ''
                        if not command['alias']:
                            text = f"{text}**!{command['name']}"
                        else:
                            text = f"{text}**!{command['name']}/{'/'.join(command['alias'])}"
                        if command['usage'] == "":
                            text = f"{text}**\n```{command['desc']}\nExample: {command['example']}```\n"
                        else:
                            text = f"{text} {command['usage']}**\n```{command['desc']}\n" \
                                   f"Example: {command['example']}```\n"

                        for sim_cmd in help_dict[f"{cog}"]:
                            if command['name'][0:4] in sim_cmd['name'] and \
                                    command['name'] != sim_cmd['name']:
                                if not sim_cmd['alias']:
                                    text2 = f"{text2}**!{sim_cmd['name']}"
                                else:
                                    text2 = f"{text2}**!{sim_cmd['name']}/{'/'.join(sim_cmd['alias'])}"
                                if sim_cmd['usage'] == "":
                                    text2 = f"{text2}**\n```{sim_cmd['desc']}\nExample: {sim_cmd['example']}```\n"
                                else:
                                    text2 = f"{text2} {sim_cmd['usage']}**\n```{sim_cmd['desc']}\n" \
                                            f"Example: {sim_cmd['example']}```\n"

                        help_embed = discord.Embed(title="Thorny Help Center",
                                                   description="Use `!help [command]` to see specific commands\n"
                                                               "Do not include brackets in commands, they just show the"
                                                               " `[optional]` and `<required>` fields of a command",
                                                   color=0x65b39b)
                        help_embed.add_field(name=f"\u200b", value=f"{text}")
                        if text2 != '':
                            help_embed.add_field(name=f"**Similar Commands to !{cmd}**", value=f"{text2}",
                                                 inline=False)
                        await ctx.send(embed=help_embed)

        else:
            await ctx.send(f"Hmm... Looks like this command doesn't exist, or you didn't Capitalize the Category!")

    @help.command(help="Get help on editing the Kingdom Command")
    async def kingdoms(self, ctx):
        help_embed = discord.Embed(colour=0x65b39b)
        help_embed.add_field(name=":question: **Kingdom Help**",
                             value=f"**!kedit <field> <value>** - Edit a certain field on the command!")
        help_embed.add_field(name=":pencil: **Fields You Can Edit**",
                             value=f"You can edit the following fields (In order from top to bottom):\n\n"
                                   f"**Slogan** - The top part of the kingdom command | Max. 5 words\n"
                                   f"**Ruler** - Your Kingdom's Ruler\n"
                                   f"**Capital** - The Capital CIty | Max. 30 characters\n"
                                   f"**Border_type** - Open, Closed, Partially Open | Max. 30 characters\n"
                                   f"**Gov_type** - Kingdom's Government Type\n"
                                   f"**Alliances** - Your kingdom's alliances | Max. 50 characters\n"
                                   f"**Description** - Your Kingdom's Description | Max. 30 words\n"
                                   f"**Lore** - Your Kingdom's Lore | Max. 30 words",
                             inline=False)
        help_embed.set_footer(text=f"Use !help kingdoms to access this!")
        await ctx.send(embed=help_embed)

    @commands.command(help="Get a random tip!")
    async def tip(self, ctx, number=None):
        tip = json.load(open('./../thorny_data/tips.json', 'r'))
        tip_embed = discord.Embed(color=0x65b39b)
        if number is None:
            number = str(random.randint(1, len(tip['tips'])))
        tip_embed.add_field(name=f"Pro Tip!",
                            value=tip['tips'][number])
        tip_embed.set_footer(text=f"Tip {number}/{len(tip['tips'])} | Use !tip [number] to get a tip!")
        await ctx.send(embed=tip_embed)

    @commands.command(aliases=["form"], help="Get a link to the EverForms")
    async def everforms(self, ctx):
        await ctx.send(f"**Here's a link!**\n"
                       f"EverForms is the unified way to submit different forms!\n"
                       f"https://forms.gle/kTaB7NN2gkpzWmcs7")
