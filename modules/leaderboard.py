import random
from datetime import datetime
import discord
from discord.ext import commands
import json

from functions import write_log, process_json, total_json, reset_values
from functions import profile_update


class Leaderboards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['lb'], invoke_without_command=True)
    async def leaderboard(self, ctx):
        await ctx.send('> **Available Leaderboards**\n'
                       '\n**!lb activity [month] [page]** • Shows activity for all players | Also: !act'
                       "\n**!lb nugs [page]** • Shows a leaderboard of people's nugs | Also: !money"
                       '\n**!lb treasuries** • Shows the balance of all treasuries | Also: !tries'
                       '\n\n*When writing commands, do not include [the brackets]*')

    @leaderboard.command(aliases=['act'])
    async def activity(self, ctx, month=None, page=1):
        if month is None:
            month = datetime.now().strftime("%B").lower()
        if month.lower() in 'july' or month.lower() in 'august':
            temp = ''''''
            print(f'Activity gotten on {datetime.now().strftime("%B %d, %Y, %H:%M:%S")}')
            file = open(f'./../thorny_data/processed_{month[0:3]}21.txt', 'r')
            for line in file:
                temp = f'''{temp}{line}'''
            embed = discord.Embed(title=f'**ACTIVITY FOR {month.upper()}**', color=0xB4C424)
            embed.add_field(name=f'*Here is a list of the activity from {month} 1st*', value=f"{temp}")
            embed.set_footer(text="Fun Fact: This command is from Thorny v0.2")
            await ctx.send(embed=embed)
        else:
            try:
                int(month)
            except ValueError:
                if page == 1:
                    start = 0
                    stop = 20
                else:
                    start = (int(page) - 1) * 20
                    stop = start + 20

                lb_to_send = ''
                print(f'Activity gotten on {datetime.now()}')
                if month.lower() in datetime.now().strftime("%B").lower():
                    reset_values()
                    process_json(month[0:3])
                    total_json(month[0:3], ctx.author)
                lb_file = open(f'./../thorny_data/leaderboard_{month[0:3]}21.json', 'r+')
                lb_json = json.load(lb_file)

                if start > len(lb_json):
                    error_embed = discord.Embed(color=0x900C3F)
                    error_embed.add_field(name='Woah Woah There',
                                          value='We do not have enough users to get to *that* page bro!')
                    await ctx.send(embed=error_embed)
                else:
                    for rank in lb_json[start:stop]:
                        if month.lower() in 'september':
                            lb_to_send = f'{lb_to_send}\n' \
                                         f'**{lb_json.index(rank) + 1}.** ' \
                                         f'<@{rank["name"]}> • **{rank["time_played"]}h**'
                        else:
                            lb_to_send = f'{lb_to_send}\n' \
                                         f'**{lb_json.index(rank) + 1}.** <@{rank["name"]}> • ' \
                                         f'**{rank["time_played"].split(":")[0]}h{rank["time_played"].split(":")[1]}m**'

                lb_embed = discord.Embed(title=f'**Activity Leaderboard {month.capitalize()}**',
                                         color=0x6495ED)
                lb_embed.add_field(name=f'\u200b',
                                   value=f"{lb_to_send}")
                lb_embed.set_footer(text=f'Page {page}/{round(len(lb_json)/20)} | Use !leaderboard to see others')
                await ctx.send(embed=lb_embed)
            else:
                error_embed = discord.Embed(color=0x900C3F)
                error_embed.add_field(name='Ahhhhhh, I see the problem!',
                                      value='To flip through pages, you gotta write the **month** and then the page!'
                                            f'\nSo try this: !lb activity {datetime.now().strftime("%B")} {month}')
                await ctx.send(embed=error_embed)

    @leaderboard.command(aliases=['money'])
    async def nugs(self, ctx, page=1):
        if page == 1:
            start = 0
            stop = 10
        else:
            start = (int(page)-1)*10
            stop = start+10

        lb_to_send = ''
        profile_file = open('./../thorny_data/profiles.json', 'r')
        profile_dict = json.load(profile_file)
        profile_list = []
        for dict in profile_dict:
            profile_list.append({"user": dict, "balance": profile_dict[f"{dict}"]["balance"]})
        profile_sorted = sorted(profile_list, key=lambda x: (x["balance"]), reverse=True)[:-1]

        if start > len(profile_sorted):
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Woah Woah There',
                                  value='We do not have enough users to get to *that* page bro!')
            await ctx.send(embed=error_embed)
        else:
            for entry in profile_sorted[start:stop]:
                lb_to_send = f'{lb_to_send}\n' \
                             f'**{profile_sorted.index(entry) + 1}.**  <@{entry["user"]}> • ' \
                             f'<:Nug:884320353202081833>**{entry["balance"]}**'

            lb_embed = discord.Embed(title=f'**Nugs Leaderboard**',
                                     color=0x6495ED)
            lb_embed.add_field(name=f'\u200b',
                               value=f"{lb_to_send}")
            lb_embed.set_footer(text=f'Page {page}/{round(len(profile_sorted)/10)} | Use !leaderboard to see others')
            await ctx.send(embed=lb_embed)

    @leaderboard.command(aliases=['tries'])
    async def treasuries(self, ctx):
        kingdom_file = open('./../thorny_data/kingdoms.json', 'r')
        kingdom_dict = json.load(kingdom_file)
        lb_to_send = f'Ambria • **<:Nug:884320353202081833>{kingdom_dict["ambria"]}**\n' \
                     f'Asbahamael • **<:Nug:884320353202081833>{kingdom_dict["asbahamael"]}**\n' \
                     f'Eireann • **<:Nug:884320353202081833>{kingdom_dict["eireann"]}**\n' \
                     f'Dalvasha • **<:Nug:884320353202081833>{kingdom_dict["dalvasha"]}**\n' \
                     f'Stregabor • **<:Nug:884320353202081833>{kingdom_dict["stregabor"]}**\n'

        lb_embed = discord.Embed(title=f'**Kingdom Treasuries**',
                                 color=0x6495ED)
        lb_embed.add_field(name=f'\u200b',
                           value=f"{lb_to_send}")
        lb_embed.set_footer(text=f'Page 1/1 | Use !leaderboard to see others')
        await ctx.send(embed=lb_embed)