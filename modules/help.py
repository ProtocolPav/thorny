from datetime import datetime, timedelta
import discord
from discord.ext import commands
import errors


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['hlp'], invoke_without_command=True, help="Helps You A Lot")
    async def help(self, ctx, cmd=None, subcmd=None):
        if cmd is None:
            commands_dict = {}
            for cog in self.client.cogs:
                commands_dict[f"{cog}"] = []
                for command in self.client.get_cog(cog).get_commands():
                    if isinstance(command, commands.Group):
                        if command.signature == "":
                            commands_dict[f"{cog}"].append([f"{command.name}", command.help])
                        else:
                            commands_dict[f"{cog}"].append([f"{command.name} {command.signature}", command.help])
                        for subcommand in command.walk_commands():
                            if subcommand.signature == "":
                                commands_dict[f"{cog}"].append([f"{command.name} {subcommand.name}", command.help])
                            else:
                                commands_dict[f"{cog}"].append([f"{command.name} {subcommand.name} "
                                                                f"{subcommand.signature}", command.help])
                                print(command.signature)
                    else:
                        if command.signature == "":
                            commands_dict[f"{cog}"].append([f"{command.name}", command.help])
                        else:
                            commands_dict[f"{cog}"].append([f"{command.name} {command.signature}", command.help])
            sendhelp = ''
            for cog in self.client.cogs:
                n = '\n'
                sendhelp = f"{sendhelp}\n**{cog} Commands:**\n{n.join(map(str, commands_dict[f'{cog}']))}\n"
            await ctx.send(f"**BETA**\n\n{sendhelp}")
        else:
            found = False
            if subcmd is None:
                for command in self.client.commands:
                    if cmd == command.name:
                        if command.signature == "":
                            await ctx.send(f"{ctx.prefix}{command.name}- {command.help}")
                        else:
                            await ctx.send(f"{ctx.prefix}{command.name} {command.signature} - {command.help}")
                        found = True
            else:
                for command in self.client.commands:
                    if cmd == command.name:
                        for subcommand in command.walk_commands():
                            if subcmd == subcommand.name:
                                if subcommand.signature == "":
                                    await ctx.send(f"{ctx.prefix}{command.name} {subcommand.name}/{subcommand.aliases} "
                                                   f"- {subcommand.help}")
                                else:
                                    await ctx.send(f"{ctx.prefix}{command.name} {subcommand.name}/{subcommand.aliases} "
                                                   f"{subcommand.signature} - {subcommand.help}")
                                found = True
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
        await ctx.send(embed=help_embed)

