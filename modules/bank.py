import discord
from discord.ext import commands
import json
from modules import leaderboard
from functions import profile_update
import errors


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bal'], help="Checks your or a user's balance")
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        profile_update(user)
        kingdom = 'None'
        kingdoms_list = ['Stregabor', 'Ambria', 'Eireann', 'Dalvasha', 'Asbahamael']
        for item in kingdoms_list:
            if discord.utils.find(lambda r: r.name == item, ctx.message.guild.roles) in user.roles:
                kingdom = item.lower()
                profile_update(user, kingdom, "kingdom")

        profile_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        kingdom_file = open('./../thorny_data/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)

        if kingdom == 'None':
            await ctx.send(embed=errors.Pay.balance_error)
        else:
            bal_embed = discord.Embed(color=0xF4C430)
            bal_embed.set_author(name=user, icon_url=user.avatar_url)
            bal_embed.add_field(name=f'**Nugs:**',
                                value=f"<:Nug:884320353202081833>{profile[f'{user.id}']['balance']}")
            bal_embed.add_field(name=f'**{kingdom.capitalize()} Treasury**:',
                                value=f"**<:Nug:884320353202081833>{kingdom_json[kingdom]}**",
                                inline=False)
            await ctx.send(embed=bal_embed)

    @commands.command(aliases=['amoney'], help="CM Only | Add money to a player's balance")
    @commands.has_permissions(administrator=True)
    async def addmoney(self, ctx, user: discord.User, amount):
        profile_update(user)
        profile_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{user.id}']['balance'] + int(amount)
        profile_update(user, int(amount), 'balance')
        await ctx.send(f"{user}'s balance is now {amount}")

    @commands.command(aliases=['rmoney'], help="CM Only | Remove money from a player's balance")
    @commands.has_permissions(administrator=True)
    async def removemoney(self, ctx, user: discord.User, amount):
        profile_update(user)
        profile_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{user.id}']['balance'] - int(amount)
        profile_update(user, int(amount), 'balance')
        await ctx.send(f"{user}'s balance is now {amount}")

    @commands.command(help="Pay a player using nugs")
    async def pay(self, ctx, user: discord.User, amount=None, *reason):
        if ctx.channel == self.client.get_channel(700293298652315648):
            profile_file = open('./../thorny_data/profiles.json', 'r+')
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

                        pay_embed = discord.Embed(color=0xF4C430)
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

    @commands.group(aliases=['tres'], invoke_without_command=True, help="See all available actions for the Treasury")
    async def treasury(self, ctx, action=None):
        treasury_embed = discord.Embed(title="Treasury Help", color=0xCF9FFF)
        treasury_embed.add_field(name="Here are all the treasury commands you can do!",
                                 value="**!treasury store <amount>** • Store money in your kingdom's treasury!\n"
                                       "**!treasury search** • Equivalent to **!lb treasuries**\n"
                                       "**!treasury take <amount>** • Take money from the treasury (RULERS ONLY)\n"
                                       "**!treasury spend <user> <amount> [reason]** • Pay someone using "
                                       "treasury funds (RULERS ONLY)\n\n"
                                       "You can also use **!tres** instead of !treasury!")
        await ctx.send(embed=treasury_embed)

    @treasury.command(help="Store money in your kingdom's treasury")
    async def store(self, ctx, amount=None):
        kingdom_file = open('./../thorny_data/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
        profile_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)

        kingdom = 'None'
        kingdoms_list = ['Stregabor', 'Ambria', 'Eireann', 'Dalvasha', 'Asbahamael']
        for item in kingdoms_list:
            if discord.utils.find(lambda r: r.name == item, ctx.message.guild.roles) in ctx.author.roles:
                kingdom = item.lower()

        if profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0:
            amount1 = profile[f'{ctx.author.id}']['balance'] - int(amount)
            profile_update(ctx.author, amount1, 'balance')
            kingdom_json[kingdom] = kingdom_json[kingdom] + int(amount)
            kingdom_file.truncate(0)
            kingdom_file.seek(0)
            json.dump(kingdom_json, kingdom_file, indent=3)

            pay_embed = discord.Embed(color=0xE49B0F)
            pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            pay_embed.add_field(name='<:Nug:884320353202081833> Storage Successful!',
                                value=f'Amount stored: **<:Nug:884320353202081833>{amount}**\n'
                                      f'Stored in: **{kingdom.upper()} TREASURY**\n')
            await ctx.send(embed=pay_embed)

        elif profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
            await ctx.send(embed=errors.Treasury.store_lack_nugs_error)

    @treasury.command(help="Equivalent to !lb treasuries")
    async def search(self, ctx):
        await Leaderboards.treasuries(self, ctx)

    @treasury.command(help="Ruler Only | Take money from the treasury")
    @commands.has_role('Ruler')
    async def take(self, ctx, amount=None):
        kingdom_file = open('./../thorny_data/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
        profile_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)

        kingdom = 'None'
        kingdoms_list = ['Stregabor', 'Ambria', 'Eireann', 'Dalvasha', 'Asbahamael']
        for item in kingdoms_list:
            if discord.utils.find(lambda r: r.name == item, ctx.message.guild.roles) in ctx.author.roles:
                kingdom = item.lower()

        if int(amount) < 0:
            await ctx.send(embed=errors.Treasury.negative_nugs_error)

        elif kingdom_json[kingdom] - int(amount) >= 0:
            amount1 = profile[f'{ctx.author.id}']['balance'] + int(amount)
            profile_update(ctx.author, amount1, 'balance')
            kingdom_json[kingdom] = kingdom_json[kingdom] - int(amount)
            kingdom_file.truncate(0)
            kingdom_file.seek(0)
            json.dump(kingdom_json, kingdom_file, indent=3)

            pay_embed = discord.Embed(color=0xE49B0F)
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

    @treasury.command(help="Ruler Only | Pay someone using treasury funds")
    @commands.has_role('Ruler')
    async def spend(self, ctx, user: discord.User, amount=None, *reason):
        profile_file = open('./../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        kingdom_file = open('./../thorny_data/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)

        kingdom = 'None'
        kingdoms_list = ['Stregabor', 'Ambria', 'Eireann', 'Dalvasha', 'Asbahamael']
        for item in kingdoms_list:
            if discord.utils.find(lambda r: r.name == item, ctx.message.guild.roles) in ctx.author.roles:
                kingdom = item.lower()

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

                pay_embed = discord.Embed(color=0xE49B0F)
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