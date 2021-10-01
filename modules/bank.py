import random
from datetime import datetime

import discord
from discord.ext import commands
import json
from thornyv1_3.modules.leaderboard import Leaderboards
from thornyv1_3.activity import profile_update
from thornyv1_3 import errors
thorny = commands.Bot(command_prefix='!')


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user: discord.Member = None):
        kingdom = ''
        if user is None:
            profile_update(ctx.author)
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
        else:
            profile_update(user)
            if discord.utils.find(lambda r: r.name == 'Stregabor', ctx.message.guild.roles) in user.roles:
                kingdom = 'stregabor'
            elif discord.utils.find(lambda r: r.name == 'Ambria', ctx.message.guild.roles) in user.roles:
                kingdom = 'ambria'
            elif discord.utils.find(lambda r: r.name == 'Eireann', ctx.message.guild.roles) in user.roles:
                kingdom = 'eireann'
            elif discord.utils.find(lambda r: r.name == 'Dalvasha', ctx.message.guild.roles) in user.roles:
                kingdom = 'dalvasha'
            elif discord.utils.find(lambda r: r.name == 'Asbahamael', ctx.message.guild.roles) in user.roles:
                kingdom = 'asbahamael'
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        kingdom_file = open('text files/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
        if kingdom == '':
            await ctx.send(embed=errors.Pay.balance_error)
        else:
            if user is None:
                lb_embed = discord.Embed(color=0xDAA520)
                lb_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                lb_embed.add_field(name=f'**Nugs:**',
                                   value=f"<:Nug:884320353202081833>{profile[f'{ctx.author.id}']['balance']}")
                lb_embed.add_field(name=f'**{kingdom.capitalize()} Treasury**:',
                                   value=f"**<:Nug:884320353202081833>{kingdom_json[kingdom]}**",
                                   inline=False)
                await ctx.send(embed=lb_embed)
            else:
                lb_embed = discord.Embed(color=0xDAA520)
                lb_embed.set_author(name=f'{user}', icon_url=f'{user.avatar_url}')
                lb_embed.add_field(name=f'**Nugs:**',
                                   value=f"<:Nug:884320353202081833>{profile[f'{user.id}']['balance']}")
                lb_embed.add_field(name=f'**{kingdom.capitalize()} Treasury**:',
                                   value=f"**<:Nug:884320353202081833>{kingdom_json[kingdom]}**",
                                   inline=False)
                await ctx.send(embed=lb_embed)

    @commands.command(aliases=['amoney'])
    @commands.has_permissions(administrator=True)
    async def addmoney(self, ctx, user: discord.User, amount):
        profile_update(user)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{user.id}']['balance'] + int(amount)
        profile_update(user, int(amount), 'balance')
        await ctx.send(f"{user}'s balance is now {amount}")

    @commands.command(aliases=['rmoney'])
    @commands.has_permissions(administrator=True)
    async def removemoney(self, ctx, user: discord.User, amount):
        profile_update(user)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{user.id}']['balance'] - int(amount)
        profile_update(user, int(amount), 'balance')
        await ctx.send(f"{user}'s balance is now {amount}")

    @commands.command()
    async def pay(self, ctx, user: discord.User, amount=None, *reason):
        if ctx.channel == thorny.get_channel(700293298652315648):
            profile_file = open('text files/profiles.json', 'r+')
            profile = json.load(profile_file)
            if user == ctx.author:
                await ctx.send(embed=errors.Pay.self_error)
            elif amount is None:
                await ctx.send(embed=errors.Pay.amount_error)
            elif str(ctx.author.id) not in profile:
                await ctx.send(embed=errors.Pay.self_register_error)
            elif profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
                await ctx.send(embed=errors.Pay.lack_nugs_error)

            elif str(ctx.author.id) in profile:
                if int(amount) > 0:
                    if profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0 and user != ctx.author:
                        amount1 = profile[f'{ctx.author.id}']['balance'] - int(amount)
                        profile_update(ctx.author, amount1, 'balance')
                        amount2 = profile[f'{user.id}']['balance'] + int(amount)
                        profile_update(user, amount2, 'balance')

                        pay_embed = discord.Embed(color=0xDAA520)
                        pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                        pay_embed.add_field(name='<:Nug:884320353202081833> Payment Successful!',
                                            value=f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                                  f'Paid to: **{user.mention}**\n'
                                                  f'\n**Reason: {" ".join(str(x) for x in reason)}**')
                        await ctx.send(embed=pay_embed)
                else:
                    await ctx.send(embed=errors.Pay.negative_nugs_error)
        else:
            await ctx.send(embed=errors.Pay.channel_error)

    @commands.group(aliases=['tres'], invoke_without_command=True)
    async def treasury(self, ctx):
        await ctx.send('Use !help treasury to see all available sub-commands!')

    @treasury.command()
    async def store(self, ctx, amount=None):
        kingdom_file = open('text files/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
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

        if profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0:
            amount1 = profile[f'{ctx.author.id}']['balance'] - int(amount)
            profile_update(ctx.author, amount1, 'balance')
            kingdom_json[kingdom] = kingdom_json[kingdom] + int(amount)
            kingdom_file.truncate(0)
            kingdom_file.seek(0)
            json.dump(kingdom_json, kingdom_file, indent=3)

            pay_embed = discord.Embed(color=0xF88379)
            pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            pay_embed.add_field(name='<:Nug:884320353202081833> Storage Successful!',
                                value=f'Amount stored: **<:Nug:884320353202081833>{amount}**\n'
                                      f'Stored in: **{kingdom.upper()} TREASURY**\n')
            await ctx.send(embed=pay_embed)

        elif profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
            await ctx.send(embed=errors.Treasury.store_lack_nugs_error)

    @treasury.command()
    async def search(self, ctx):
        await Leaderboards.treasuries(self, ctx)

    @treasury.command()
    @commands.has_role('Ruler')
    async def take(self, ctx, amount=None):
        kingdom_file = open('text files/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
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

        if int(amount) < 0:
            await ctx.send(embed=errors.Treasury.negative_nugs_error)

        elif kingdom_json[kingdom] - int(amount) >= 0:
            amount1 = profile[f'{ctx.author.id}']['balance'] + int(amount)
            profile_update(ctx.author, amount1, 'balance')
            kingdom_json[kingdom] = kingdom_json[kingdom] - int(amount)
            kingdom_file.truncate(0)
            kingdom_file.seek(0)
            json.dump(kingdom_json, kingdom_file, indent=3)

            pay_embed = discord.Embed(color=0xFF7F50)
            pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            pay_embed.add_field(name='<:Nug:884320353202081833> Taking Successful!',
                                value=f'Amount taken: **<:Nug:884320353202081833>{amount}**\n'
                                      f'Taken from: **{kingdom.upper()} TREASURY**\n')
            await ctx.send(embed=pay_embed)

        elif profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
            await ctx.send(embed=errors.Treasury.take_lack_nugs_error)

    @take.error
    async def take_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=errors.Treasury.ruler_error)

    @treasury.command()
    @commands.has_role('Ruler')
    async def spend(self, ctx, user: discord.User, amount=None, *reason):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        kingdom_file = open('text files/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
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

        if user == ctx.author:
            await ctx.send(embed=errors.Pay.self_error)
        elif amount is None:
            await ctx.send(embed=errors.Pay.amount_error)
        elif str(ctx.author.id) not in profile:
            await ctx.send(embed=errors.Pay.self_register_error)
        elif kingdom_json[kingdom] - int(amount) < 0:
            await ctx.send(embed=errors.Pay.lack_nugs_error)

        elif str(ctx.author.id) in profile:
            if kingdom_json[kingdom] - int(amount) >= 0 and user != ctx.author:
                kingdom_json[kingdom] = kingdom_json[kingdom] - int(amount)
                kingdom_file.truncate(0)
                kingdom_file.seek(0)
                json.dump(kingdom_json, kingdom_file, indent=3)

                amount2 = profile[f'{user.id}']['balance'] + int(amount)
                profile_update(user, amount2, 'balance')

                pay_embed = discord.Embed(color=0xFF7F50)
                pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                pay_embed.add_field(name='<:Nug:884320353202081833> Treasury Payment Successful!',
                                    value=f'From the **{kingdom.upper()} TREASURY**\n'
                                          f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Paid to: **{user.mention}**\n'
                                          f'\n**Reason: {" ".join(str(x) for x in reason)}**\n')
                await ctx.send(embed=pay_embed)

    @spend.error
    async def spend_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=errors.Treasury.ruler_error)