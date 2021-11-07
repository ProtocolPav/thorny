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

    @commands.group(aliases=['hlp', 'ask'], invoke_without_command=True, help="Access the Thorny Help Center")
    async def help(self, ctx, cmd=None):
        help_dict = {"CM": {}}
        for cog in self.client.cogs:
            help_dict[f"{cog}"] = {}
            cmd_num = 1
            hidden_num = 1
            for command in self.client.get_cog(cog).get_commands():
                if isinstance(command, commands.Group):
                    if command.signature == "" and not command.hidden:
                        help_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                             "usage": "",
                                                             "alias": command.aliases,
                                                             "desc": command.help}
                    elif not command.hidden:
                        help_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                             "usage": command.signature,
                                                             "alias": command.aliases,
                                                             "desc": command.help}
                    else:
                        cmd_num -= 1
                        help_dict["CM"][str(hidden_num)] = {"name": command.name,
                                                            "usage": command.signature,
                                                            "alias": command.aliases,
                                                            "desc": command.help}
                        hidden_num += 1
                    for subcommand in command.walk_commands():
                        cmd_num += 1
                        if subcommand.signature == "" and not command.hidden:
                            help_dict[f"{cog}"][str(cmd_num)] = {"name": f"{command.name} {subcommand.name}",
                                                                 "usage": "",
                                                                 "alias": subcommand.aliases,
                                                                 "desc": subcommand.help}
                        elif not command.hidden:
                            help_dict[f"{cog}"][str(cmd_num)] = {"name": f"{command.name} {subcommand.name}",
                                                                 "usage": subcommand.signature,
                                                                 "alias": subcommand.aliases,
                                                                 "desc": subcommand.help}
                        else:
                            cmd_num -= 1
                            help_dict["CM"][str(hidden_num)] = {"name": command.name,
                                                                "usage": command.signature,
                                                                "alias": command.aliases,
                                                                "desc": command.help}
                            hidden_num += 1
                else:
                    if command.signature == "" and not command.hidden:
                        help_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                             "usage": "",
                                                             "alias": command.aliases,
                                                             "desc": command.help}
                    elif not command.hidden:
                        help_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                             "usage": command.signature,
                                                             "alias": command.aliases,
                                                             "desc": command.help}
                    else:
                        cmd_num -= 1
                        help_dict["CM"][str(hidden_num)] = {"name": command.name,
                                                            "usage": command.signature,
                                                            "alias": command.aliases,
                                                            "desc": command.help}
                        hidden_num += 1
                cmd_num += 1

        if cmd is None:
            help_embed = discord.Embed(title="Thorny Help Center",
                                       description="Use `!help [command]` to see specific commands\n"
                                                   "Use `!help [Category]` to see specific categories! (Capitalize)",
                                       color=0xCF9FFF)
            help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
            for cog in self.client.cogs:
                if cog == "CM":
                    pass
                else:
                    if len(help_dict[f"{cog}"]) == 3:
                        help_embed.add_field(name=f"**{cog} Commands**",
                                             value=f"```!{help_dict[f'{cog}']['1']['name']}, "
                                                   f"!{help_dict[f'{cog}']['2']['name']}, "
                                                   f"!{help_dict[f'{cog}']['3']['name']}```",
                                             inline=False)
                    else:
                        help_embed.add_field(name=f"**{cog} Commands**",
                                             value=f"```!{help_dict[f'{cog}']['1']['name']}, "
                                                   f"!{help_dict[f'{cog}']['2']['name']}, "
                                                   f"!{help_dict[f'{cog}']['3']['name']}, "
                                                   f"!{help_dict[f'{cog}']['4']['name'][0:3]}...```",
                                             inline=False)
            await ctx.send(embed=help_embed)

        elif cmd in self.client.cogs or cmd == 'CM':
            help_embed = discord.Embed(title="Thorny Help Center",
                                       description="Use `!help [command]` to see specific commands\n\n"
                                                   "Do not include brackets in commands, they just show which"
                                                   " fields are optional to put and which are not.\n"
                                                   "`<fields>` in these must be included, `[fields]` in these are "
                                                   "optional.",
                                       color=0xCF9FFF)
            text = ''
            for command in help_dict[f'{cmd}']:
                command = help_dict[f'{cmd}'][command]
                if not command['alias']:
                    text = f"{text}**!{command['name']}"
                else:
                    text = f"{text}**!{command['name']}/{'/'.join(command['alias'])}"
                if command['usage'] == "":
                    text = f"{text}**\n```{command['desc']}```\n"
                else:
                    text = f"{text} {command['usage']}**\n```{command['desc']}```\n"
            help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
            help_embed.add_field(name=f"**{cmd} Commands**",
                                 value=f"{text}")
            await ctx.send(embed=help_embed)

        elif cmd == cmd.lower():
            for cog in self.client.cogs:
                for command in help_dict[f"{cog}"]:
                    cmd_dict = help_dict[f"{cog}"][command]
                    if cmd == cmd_dict['name'] or cmd in cmd_dict['alias']:
                        command = help_dict[f'{cog}'][command]
                        text = ''
                        text2 = ''
                        if not command['alias']:
                            text = f"{text}**!{command['name']}"
                        else:
                            text = f"{text}**!{command['name']}/{'/'.join(command['alias'])}"
                        if command['usage'] == "":
                            text = f"{text}**\n```{command['desc']}```\n"
                        else:
                            text = f"{text} {command['usage']}**\n```{command['desc']}```\n"

                        for similar_command in help_dict[f"{cog}"]:
                            if command['name'][0:4] in help_dict[f"{cog}"][similar_command]['name'] and \
                                    command['name'] != help_dict[f"{cog}"][similar_command]['name']:
                                sim_cmd = help_dict[f"{cog}"][similar_command]
                                if not sim_cmd['alias']:
                                    text2 = f"{text2}**!{sim_cmd['name']}"
                                else:
                                    text2 = f"{text2}**!{sim_cmd['name']}/{'/'.join(sim_cmd['alias'])}"
                                if sim_cmd['usage'] == "":
                                    text2 = f"{text2}**\n```{sim_cmd['desc']}```\n"
                                else:
                                    text2 = f"{text2} {sim_cmd['usage']}**\n```{sim_cmd['desc']}```\n"

                        help_embed = discord.Embed(title="Thorny Help Center",
                                                   description="Use `!help [command]` to see specific commands\n\n"
                                                               "Do not include brackets in commands, they just "
                                                               "show which fields are optional to put and which "
                                                               "are not.\n`<fields>` in these must be included, "
                                                               "`[fields]` in these are optional",
                                                   color=0xCF9FFF)
                        help_embed.add_field(name=f"\u200b", value=f"{text}")
                        if text2 != '':
                            help_embed.add_field(name=f"**Similar Commands to !{cmd}**", value=f"{text2}",
                                                 inline=False)
                        await ctx.send(embed=help_embed)

        else:
            await ctx.send(f"Hmm... Looks like this command doesn't exist, or you didn't Capitalize the Category!")

    @help.command()
    async def kingdoms(self, ctx):
        help_embed = discord.Embed(colour=0xCF9FFF)
        help_embed.add_field(name=":question: **Kingdom Help**",
                             value=f"**!your_kingdom** - View a kingdom's command! (Asba, Ambria, Streg, Dal, Eir)\n"
                                   f"**!kedit <field> <value>** - Edit a certain field on the command!")
        help_embed.add_field(name=":pencil: **Fields You Can Edit**",
                             value=f"You can edit the following fields (In order from top to bottom):\n\n"
                                   f"**Slogan** - The top part of the kingdom command | Max. 5 words\n"
                                   f"**Ruler** - Your Kingdom's Ruler\n"
                                   f"**Capital** - The Capital CIty | Max. 30 characters\n"
                                   f"**Borders** - Open, Closed, Partially Open | Max. 30 characters\n"
                                   f"**Government** - Kingdom's Government Type\n"
                                   f"**Alliances** - Your kingdom's alliances | Max. 50 characters\n"
                                   f"**Wiki** - Kingdom's Wiki Article | Send in the whole link!\n"
                                   f"**Description** - Your Kingdom's Description | Max. 30 words\n"
                                   f"**Lore** - Your Kingdom's Lore | Max. 30 words",
                             inline=False)
        help_embed.set_footer(text=f"Use !help kingdoms to access this!")
        await ctx.send(embed=help_embed)

    @commands.command()
    async def tip(self, ctx, number=None):
        tip = json.load(open('./../thorny_data/tips.json', 'r'))
        tip_embed = discord.Embed(color=0xCF9FFF)
        if number is None:
            number = str(random.randint(1,len(tip['tips'])))
        tip_embed.add_field(name=f"Pro Tip!",
                            value=tip['tips'][number])
        tip_embed.set_footer(text=f"Tip {number}/{len(tip['tips'])} | Use !tip [number] to get a tip!")
        await ctx.send(embed=tip_embed)

