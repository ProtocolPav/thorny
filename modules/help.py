from datetime import datetime, timedelta
import discord
from discord.ext import commands
import errors
import json

v = json.load(open('version.json', 'r'))['version']


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['hlp'], invoke_without_command=True, help="Helps You A Lot")
    async def help(self, ctx, cmd=None, subcmd=None):
        commands_dict = {}
        for cog in self.client.cogs:
            commands_dict[f"{cog}"] = {}
            cmd_num = 1
            for command in self.client.get_cog(cog).get_commands():
                if isinstance(command, commands.Group):
                    if command.signature == "":
                        commands_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                                 "usage": "",
                                                                 "alias": command.aliases,
                                                                 "desc": command.help}
                    else:
                        commands_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                                 "usage": command.signature,
                                                                 "alias": command.aliases,
                                                                 "desc": command.help}
                    for subcommand in command.walk_commands():
                        cmd_num += 1
                        if subcommand.signature == "":
                            commands_dict[f"{cog}"][str(cmd_num)] = {"name": f"{command.name} {subcommand.name}",
                                                                     "usage": "",
                                                                     "alias": subcommand.aliases,
                                                                     "desc": subcommand.help}
                        else:
                            commands_dict[f"{cog}"][str(cmd_num)] = {"name": f"{command.name} {subcommand.name}",
                                                                     "usage": subcommand.signature,
                                                                     "alias": subcommand.aliases,
                                                                     "desc": subcommand.help}
                else:
                    if command.signature == "":
                        commands_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                                 "usage": "",
                                                                 "alias": command.aliases,
                                                                 "desc": command.help}
                    else:
                        commands_dict[f"{cog}"][str(cmd_num)] = {"name": command.name,
                                                                 "usage": command.signature,
                                                                 "alias": command.aliases,
                                                                 "desc": command.help}
                cmd_num += 1

        if cmd is None:
            help_embed = discord.Embed(title="Thorny Help Center",
                                       description="Use `!help [command] [subcommand]` to see specific commands\n"
                                                   "Use `!help [Category]` to see specific categories! (Capitalize)",
                                       color=0xCF9FFF)
            help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
            for cog in self.client.cogs:
                if cog == "Help":
                    pass
                else:
                    if len(commands_dict[f"{cog}"]) == 3:
                        help_embed.add_field(name=f"**{cog} Commands**",
                                             value=f"```!{commands_dict[f'{cog}']['1']['name']}, "
                                                   f"!{commands_dict[f'{cog}']['2']['name']}, "
                                                   f"!{commands_dict[f'{cog}']['3']['name']}```",
                                             inline=False)
                    else:
                        help_embed.add_field(name=f"**{cog} Commands**",
                                             value=f"```!{commands_dict[f'{cog}']['1']['name']}, "
                                                   f"!{commands_dict[f'{cog}']['2']['name']}, "
                                                   f"!{commands_dict[f'{cog}']['3']['name']}, "
                                                   f"!{commands_dict[f'{cog}']['4']['name'][0:3]}...```",
                                             inline=False)
            await ctx.send(embed=help_embed)
        else:
            found = False
            if cmd in self.client.cogs:
                found = True
                help_embed = discord.Embed(title="Thorny Help Center",
                                           description="Use `!help [command] [subcommand]` to see specific commands",
                                           color=0xCF9FFF)
                text = ''
                for command in commands_dict[f'{cmd}']:
                    command = commands_dict[f'{cmd}'][command]
                    text = f"{text}**!{command['name']}/{command['alias']}{command['usage']}**\n```{command['desc']}```"
                help_embed.set_footer(text=f"{v} | Always read these bottom parts, they have useful info!")
                help_embed.add_field(name=f"**{cmd} Commands**",
                                     value=f"{text}")
                await ctx.send(embed=help_embed)
            if not found:
                await ctx.send(f"Hmm... Looks like you either used an alias for the command, or it doesn't exist!")

    @help.command()
    async def profile(self, ctx):
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
                                   f"**Bio/Aboutme** - Your Bio | Max. 30 words\n"
                                   f"**Story/Lore** - Your In-Game Character Lore | Max. 30 words",
                             inline=False)
        help_embed.add_field(name=":lock_with_ink_pen: **Categories to Show/Hide**",
                             value=f"You can choose to show/hide the following categories:\n\n"
                                   f"**Information/Info** - General info about you\n"
                                   f"**Activity** - Your activity statistics\n"
                                   f"**Wiki** - Your featured wiki article\n"
                                   f"**Bio/Aboutme** - Your bio\n"
                                   f"**Story/Lore** - Your In-Game Character lore",
                             inline=False)
        help_embed.set_footer(text=f"Use !help profile to access this!")
        await ctx.send(embed=help_embed)

    @help.command()
    async def kingdoms(self, ctx):
        help_embed = discord.Embed(colour=0xCF9FFF)
        help_embed.add_field(name=":question: **Kingdom Help**",
                             value=f"**!your_kingdom** - View a kingdom's command! (Asba, Ambria, Streg, Dal, Eir)\n"
                                   f"**!your_kingdom edit <field> <value>** - Edit a certain field on the command!")
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
        help_embed.set_footer(text=f"Use !help kingdom to access this!")
        await ctx.send(embed=help_embed)
