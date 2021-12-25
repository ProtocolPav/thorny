import discord
from discord.ext import commands

import json
import errors
import logs
import functions as func
from modules import help
import dbutils

config = json.load(open("./../thorny_data/config.json", "r"))


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['bal'], help="Checks your or a user's balance", invoke_without_command=True)
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)

        file_kingdoms = open('./../thorny_data/kingdoms.json', 'r+')
        json_kingdom = json.load(file_kingdoms)

        balance_embed = discord.Embed(color=0xE0115F)
        balance_embed.set_author(name=user, icon_url=user.avatar_url)
        balance_list = dbutils.simple_select("balance", 'user', "user_id", user.id)
        financials_text = f"**Personal Balance:** <:Nug:884320353202081833>{balance_list[0][0]}"
        if kingdom != 'None':
            financials_text = f"{financials_text}\n" \
                              f"**{kingdom.capitalize()} Treasury**:<:Nug:884320353202081833>{json_kingdom[kingdom]}"
        balance_embed.add_field(name=f'**Financials:**',
                                value=financials_text)
        inventory_text = ''
        inventory_list = dbutils.simple_select("*", "inventory", "user_id", user.id)
        for item in inventory_list[0:2]:
            inventory_text = f'{inventory_text}<:_pink:921708790322192396> ' \
                             f'{item[2]} **|** {config["inv_items"][item[1]]}\n'
        if len(inventory_list) < 2:
            for item in range(0, 2 - len(inventory_list)):
                inventory_text = f'{inventory_text}<:_pink:921708790322192396> 0 **|** Empty Slot\n'
        balance_embed.add_field(name=f'**Inventory:**',
                                value=f"{inventory_text}<:_pink:921708790322192396> **Use !inv to see more!**",
                                inline=False)
        balance_embed.set_footer(text="Donate to your kingdom with !treasury store")
        await ctx.send(embed=balance_embed)

    @balance.command(aliases=['add', 'remove'], help="CM Only | Edit a player's balance (- for removal)", hidden=True)
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, user: discord.User, amount, send_message=None):
        func.profile_update(user)
        file_profiles = open('./../thorny_data/profiles.json', 'r+')
        json_profile = json.load(file_profiles)

        bank_log = self.client.get_channel(config['channels']['bank_logs'])
        await bank_log.send(embed=logs.balance_edit(ctx.author.id, user.id, amount))

        amount = json_profile[f'{user.id}']['balance'] + int(amount)
        func.profile_update(user, int(amount), 'balance')
        if send_message is None:
            await ctx.send(f"{user}'s balance is now **{amount}**")

    @commands.command(help="Pay a player using nugs", usage="<user> <amount> [reason...]")
    async def pay(self, ctx, user: discord.User, amount=None, *reason):
        if ctx.channel == self.client.get_channel(config['channels']['bank']):
            func.profile_update(ctx.author)
            func.profile_update(user)
            file_profiles = open('./../thorny_data/profiles.json', 'r+')
            json_profile = json.load(file_profiles)

            if user == ctx.author:
                await ctx.send(embed=errors.Pay.self_error)
            elif amount is None:
                await ctx.send(embed=errors.Pay.amount_error)
            elif str(ctx.author.id) not in json_profile:
                await ctx.send(embed=errors.Pay.self_register_error)
            elif json_profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
                await ctx.send(embed=errors.Pay.lack_nugs_error)

            elif str(ctx.author.id) in json_profile:
                if int(amount) > 0:
                    if json_profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0:
                        author_amount = json_profile[f'{ctx.author.id}']['balance'] - int(amount)
                        func.profile_update(ctx.author, author_amount, 'balance')
                        user_amount = json_profile[f'{user.id}']['balance'] + int(amount)
                        func.profile_update(user, user_amount, 'balance')

                        pay_embed = discord.Embed(color=0xF4C430)
                        pay_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        pay_embed.add_field(name='<:Nug:884320353202081833> Payment Successful!',
                                            value=f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                                  f'Paid to: **{user.mention}**\n'
                                                  f'\n**Reason: {" ".join(str(x) for x in reason)}**')
                        await ctx.send(embed=pay_embed)
                        bank_log = self.client.get_channel(config['channels']['bank_logs'])
                        await bank_log.send(embed=logs.transaction(ctx.author.id, user.id, amount, reason))
                else:
                    await ctx.send(embed=errors.Pay.negative_nugs_error)
        else:
            await ctx.send(embed=errors.Pay.channel_error)

    @commands.group(aliases=['tres'], invoke_without_command=True, help="See all available actions for the Treasury")
    async def treasury(self, ctx):
        await help.Help.help(self, ctx, "treasury")

    @treasury.command(help="Store money in your kingdom's treasury")
    async def store(self, ctx, amount=None):
        file_kingdoms = open('./../thorny_data/kingdoms.json', 'r+')
        json_kingdoms = json.load(file_kingdoms)
        file_profiles = open('./../thorny_data/profiles.json', 'r+')
        json_profile = json.load(file_profiles)

        kingdom = func.get_user_kingdom(ctx, ctx.author)

        if json_profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0:
            author_amount = json_profile[f'{ctx.author.id}']['balance'] - int(amount)
            func.profile_update(ctx.author, author_amount, 'balance')
            json_kingdoms[kingdom] = json_kingdoms[kingdom] + int(amount)
            file_kingdoms.truncate(0)
            file_kingdoms.seek(0)
            json.dump(json_kingdoms, file_kingdoms, indent=3)

            pay_embed = discord.Embed(color=0xE49B0F)
            pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            pay_embed.add_field(name='<:Nug:884320353202081833> Storage Successful!',
                                value=f'Amount stored: **<:Nug:884320353202081833>{amount}**\n'
                                      f'Stored in: **{kingdom.upper()} TREASURY**\n')
            await ctx.send(embed=pay_embed)

        elif json_profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
            await ctx.send(embed=errors.Treasury.store_lack_nugs_error)

    @treasury.command(help="Ruler Only | Take money from the treasury", usage="<amount>")
    @commands.has_role('Ruler')
    async def take(self, ctx, amount=None):
        file_kingdoms = open('./../thorny_data/kingdoms.json', 'r+')
        json_kingdoms = json.load(file_kingdoms)
        file_profiles = open('./../thorny_data/profiles.json', 'r+')
        json_profile = json.load(file_profiles)

        kingdom = func.get_user_kingdom(ctx, ctx.author)

        if int(amount) < 0:
            await ctx.send(embed=errors.Treasury.negative_nugs_error)

        elif json_kingdoms[kingdom] - int(amount) >= 0:
            author_amount = json_profile[f'{ctx.author.id}']['balance'] + int(amount)
            func.profile_update(ctx.author, author_amount, 'balance')
            json_kingdoms[kingdom] = json_kingdoms[kingdom] - int(amount)
            file_kingdoms.truncate(0)
            file_kingdoms.seek(0)
            json.dump(json_kingdoms, file_kingdoms, indent=3)

            pay_embed = discord.Embed(color=0xE49B0F)
            pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            pay_embed.add_field(name='<:Nug:884320353202081833> Taking Successful!',
                                value=f'Amount taken: **<:Nug:884320353202081833>{amount}**\n'
                                      f'Taken from: **{kingdom.upper()} TREASURY**\n')
            await ctx.send(embed=pay_embed)

        elif json_profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
            await ctx.send(embed=errors.Treasury.take_lack_nugs_error)

    @take.error
    async def take_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=errors.Treasury.ruler_error)

    @treasury.command(help="Ruler Only | Pay someone using treasury funds", usage="<user> <amount> [reason...]")
    @commands.has_role('Ruler')
    async def spend(self, ctx, user: discord.User, amount=None, *reason):
        if ctx.channel == self.client.get_channel(config['channels']['bank']):
            file_profiles = open('./../thorny_data/profiles.json', 'r+')
            json_profile = json.load(file_profiles)
            file_kingdoms = open('./../thorny_data/kingdoms.json', 'r+')
            json_kingdoms = json.load(file_kingdoms)
            func.profile_update(user)

            kingdom = func.get_user_kingdom(ctx, ctx.author)

            if user == ctx.author:
                await ctx.send(embed=errors.Pay.self_error)
            elif amount is None:
                await ctx.send(embed=errors.Pay.amount_error)
            elif str(ctx.author.id) not in json_profile:
                await ctx.send(embed=errors.Pay.self_register_error)
            elif json_kingdoms[kingdom] - int(amount) < 0:
                await ctx.send(embed=errors.Pay.lack_nugs_error)

            elif str(ctx.author.id) in json_profile:
                if json_kingdoms[kingdom] - int(amount) >= 0:
                    json_kingdoms[kingdom] = json_kingdoms[kingdom] - int(amount)
                    file_kingdoms.truncate(0)
                    file_kingdoms.seek(0)
                    json.dump(json_kingdoms, file_kingdoms, indent=3)

                    user_amount = json_profile[f'{user.id}']['balance'] + int(amount)
                    func.profile_update(user, user_amount, 'balance')

                    pay_embed = discord.Embed(color=0xE49B0F)
                    pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                    pay_embed.add_field(name='<:Nug:884320353202081833> Treasury Payment Successful!',
                                        value=f'From the **{kingdom.upper()} TREASURY**\n'
                                              f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                              f'Paid to: **{user.mention}**\n'
                                              f'\n**Reason: {" ".join(str(x) for x in reason)}**\n')
                    await ctx.send(embed=pay_embed)
        else:
            await ctx.send(embed=errors.Pay.channel_error)

    @spend.error
    async def spend_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=errors.Treasury.ruler_error)