import discord
from discord.ext import commands

import json
from thorny_code import errors
from thorny_code import logs
from thorny_code import functions as func
from thorny_code import dbutils
from thorny_code import dbclass as db

config = json.load(open("./../thorny_data/config.json", "r"))


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    balance = discord.SlashCommandGroup("balance", "Balance Commands")

    @balance.command(description="View someone's balance")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        thorny_user = await db.ThornyFactory.build(user)
        await thorny_user.update("kingdom", kingdom)

        personal_bal = f"**Personal Balance:** <:Nug:884320353202081833>{thorny_user.balance}"
        kingdom_bal = ''
        if kingdom is not None:
            treasury_list = await dbutils.condition_select("kingdoms", 'treasury', 'kingdom', kingdom)
            kingdom_bal = f"**{kingdom.capitalize()} Treasury:** <:Nug:884320353202081833>" \
                          f"{treasury_list[0][0]}"
        inventory_text = ''
        inventory_list = await thorny_user.inventory.get_all_slots()
        for item in inventory_list[0:2]:
            inventory_text = f'{inventory_text}<:_pink:921708790322192396> ' \
                             f'{item["item_count"]} **|** {item["display_name"]}\n'
        if len(inventory_list) < 2:
            for item in range(0, 2 - len(inventory_list)):
                inventory_text = f'{inventory_text}<:_pink:921708790322192396> Empty\n'

        balance_embed = discord.Embed(color=0xE0115F)
        balance_embed.set_author(name=user, icon_url=user.display_avatar.url)
        balance_embed.add_field(name=f'**Financials:**',
                                value=f"{personal_bal}\n{kingdom_bal}")
        balance_embed.add_field(name=f'**Inventory:**',
                                value=f"{inventory_text}<:_purple:921708790368309269> "
                                      f"**/inventory view to see more!**",
                                inline=False)
        balance_embed.set_footer(text="Donate to your kingdom with /treasury store")
        await ctx.respond(embed=balance_embed)

    @balance.command(description="CM Only | Edit a player's balance")
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, user: discord.Member, amount: discord.Option(int, "Put a - if you want to remove nugs")):
        bank_log = self.client.get_channel(config['channels']['bank_logs'])
        await bank_log.send(embed=logs.balance_edit(ctx.author.id, user.id, amount))

        thorny_user = await db.ThornyFactory.build(user)
        await thorny_user.update("balance", thorny_user.balance + amount)

        if 'edit' in ctx.command.qualified_name.lower():
            await ctx.respond(f"{user}'s balance is now **{thorny_user.balance}**! (Added/Removed: {amount})")

    @commands.slash_command(description="Pay a player using nugs")
    async def pay(self, ctx, user: discord.Member, amount: int, reason=None):
        if ctx.channel == self.client.get_channel(config['channels']['bank']):
            receivable_user = await db.ThornyFactory.build(user)
            payable_user = await db.ThornyFactory.build(ctx.author)

            if user == ctx.author:
                await ctx.respond(embed=errors.Pay.self_error, ephemeral=True)
            elif amount is None:
                await ctx.respond(embed=errors.Pay.amount_error, ephemeral=True)
            elif payable_user.balance - amount < 0:
                await ctx.respond(embed=errors.Pay.lack_nugs_error, ephemeral=True)
            elif amount > 0:
                await payable_user.update("balance", payable_user.balance - amount)
                await receivable_user.update("balance", receivable_user.balance + amount)

                pay_embed = discord.Embed(color=0xF4C430)
                pay_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
                pay_embed.add_field(name='<:Nug:884320353202081833> Payment Successful!',
                                    value=f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Paid to: **{user.mention}**\n'
                                          f'\n**Reason: {reason}**')
                await ctx.respond(f"{user.mention} You've been paid!")
                await ctx.edit(content=None, embed=pay_embed)

                bank_log = self.client.get_channel(config['channels']['bank_logs'])
                await bank_log.send(embed=logs.transaction(ctx.author.id, user.id, amount, reason))
            elif amount < 0:
                await ctx.respond(embed=errors.Pay.negative_nugs_error, ephemeral=True)
        else:
            await ctx.respond(embed=errors.Pay.channel_error, ephemeral=True)

    treasury = discord.SlashCommandGroup("treasury", "Treasury Commands")

    @treasury.command(description="Store money in your kingdom's treasury")
    async def store(self, ctx, amount: int):
        user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        thorny_user = await db.ThornyFactory.build(user)
        await thorny_user.update("kingdom", kingdom)

        if kingdom is not None:
            receivable = await dbutils.condition_select('kingdoms', 'treasury', 'kingdom', kingdom)
            receivable = receivable[0][0]

            if thorny_user.balance - amount < 0:
                await ctx.respond(embed=errors.Pay.lack_nugs_error, ephemeral=True)
            else:
                await thorny_user.update("balance", thorny_user.balance - amount)
                await dbutils.simple_update('kingdoms', 'treasury', receivable + int(amount), 'kingdom', kingdom)

                pay_embed = discord.Embed(color=0xE49B0F)
                pay_embed.set_author(name=f'{user}', icon_url=user.display_avatar.url)
                pay_embed.add_field(name='<:Nug:884320353202081833> Storage Successful!',
                                    value=f'Amount stored: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Stored in: **{kingdom} Treasury**\n')
                await ctx.respond(embed=pay_embed)
        else:
            await ctx.respond(embed=errors.Treasury.kingdom_error, ephemeral=True)

    @treasury.command(description="Ruler Only | Take money from the treasury")
    @commands.has_role('Ruler')
    async def take(self, ctx, amount: int):
        user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        thorny_user = await db.ThornyFactory.build(user)
        await thorny_user.update("kingdom", kingdom)

        payable = await dbutils.condition_select('kingdoms', 'treasury', 'kingdom', kingdom)
        payable = payable[0][0]

        if amount < 0:
            await ctx.respond(embed=errors.Pay.negative_nugs_error, ephemeral=True)
        elif payable - amount < 0:
            await ctx.respond(embed=errors.Pay.lack_nugs_error, ephemeral=True)
        elif amount is None:
            await ctx.respond(embed=errors.Pay.amount_error, ephemeral=True)
        else:
            await thorny_user.update("balance", thorny_user.balance + amount)
            await dbutils.simple_update('kingdoms', 'treasury', payable - amount, 'kingdom', kingdom)

            pay_embed = discord.Embed(color=0xE49B0F)
            pay_embed.set_author(name=f'{ctx.author}', icon_url=user.display_avatar.url)
            pay_embed.add_field(name='<:Nug:884320353202081833> Taking Successful!',
                                value=f'Amount taken: **<:Nug:884320353202081833>{amount}**\n'
                                      f'Taken from: **{kingdom} Treasury**\n')
            await ctx.respond(embed=pay_embed)

    @take.error
    async def take_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.respond(embed=errors.Treasury.ruler_error, ephemeral=True)

    # @treasury.command(description="Ruler Only | Pay someone using treasury funds")
    # @commands.has_role('Ruler')
    # async def spend(self, ctx, user: discord.Member, amount, reason):
    #     if ctx.channel == self.client.get_channel(config['channels']['bank']):
    #         kingdom = func.get_user_kingdom(ctx, ctx.author)
    #         await dbutils.simple_update('user', 'kingdom', kingdom, 'user_id', ctx.author.id)
    #
    #         if user == ctx.author:
    #             await ctx.respond(embed=errors.Pay.self_error, ephemeral=True)
    #         elif amount is None:
    #             await ctx.respond(embed=errors.Pay.amount_error, ephemeral=True)
    #         elif str(ctx.author.id) not in json_profile:
    #             await ctx.respond(embed=errors.Pay.self_register_error, ephemeral=True)
    #         elif json_kingdoms[kingdom] - int(amount) < 0:
    #             await ctx.respond(embed=errors.Pay.lack_nugs_error)
    #
    #         elif str(ctx.author.id) in json_profile:
    #             if json_kingdoms[kingdom] - int(amount) >= 0:
    #                 json_kingdoms[kingdom] = json_kingdoms[kingdom] - int(amount)
    #                 file_kingdoms.truncate(0)
    #                 file_kingdoms.seek(0)
    #                 json.dump(json_kingdoms, file_kingdoms, indent=3)
    #
    #                 user_amount = json_profile[f'{user.id}']['balance'] + int(amount)
    #                 func.profile_update(user, user_amount, 'balance')
    #
    #                 pay_embed = discord.Embed(color=0xE49B0F)
    #                 pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar}')
    #                 pay_embed.add_field(name='<:Nug:884320353202081833> Treasury Payment Successful!',
    #                                     value=f'From the **{kingdom.upper()} TREASURY**\n'
    #                                           f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
    #                                           f'Paid to: **{user.mention}**\n'
    #                                           f'\n**Reason: {" ".join(str(x) for x in reason)}**\n')
    #                 await ctx.send(embed=pay_embed)
    #     else:
    #         await ctx.send(embed=errors.Pay.channel_error)
    #
    # @spend.error
    # async def spend_error(self, ctx, error):
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.respond(embed=errors.Treasury.ruler_error, ephemeral=True)
