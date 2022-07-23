import discord
from discord.ext import commands

import json
from thorny_core import errors
from thorny_core.dbfactory import ThornyFactory
from thorny_core import functions as func
from thorny_core import dbutils
from thorny_core.dbcommit import commit
from thorny_core import dbevent as ev

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
        thorny_user = await ThornyFactory.build(user)
        thorny_user.kingdom = kingdom
        await commit(thorny_user)

        personal_bal = f"**Personal Balance:** <:Nug:884320353202081833>{thorny_user.balance}"
        kingdom_bal = ''
        if kingdom is not None:
            selector = dbutils.Base()
            treasury_list = await selector.select("treasury", "kingdoms", "kingdom", kingdom)
            kingdom_bal = f"**{kingdom.capitalize()} Treasury:** <:Nug:884320353202081833>" \
                          f"{treasury_list[0][0]}"
        inventory_text = ''
        inventory_list = thorny_user.inventory.slots
        for item in inventory_list[0:2]:
            inventory_text = f'{inventory_text}<:_pink:921708790322192396> ' \
                             f'{item.item_count} **|** {item.item_display_name}\n'
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

    @balance.command(description="CM ONLY | Edit someone's balance")
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, user: discord.Member,
                   amount: discord.Option(int, "Put a - if you want to remove nugs")):
        # bank_log = self.client.get_channel(config['channels']['bank_logs'])
        # await bank_log.send(embed=logs.balance_edit(ctx.author.id, user.id, amount))

        thorny_user = await ThornyFactory.build(user)
        thorny_user.balance += amount

        if 'edit' in ctx.command.qualified_name.lower():
            await ctx.respond(f"{user}'s balance is now **{thorny_user.balance}**! (Added/Removed: {amount})")
        await commit(thorny_user)

    @commands.slash_command(description="Pay a player using nugs")
    async def pay(self, ctx, user: discord.Member, amount: int, reason: str):
        if ctx.channel == self.client.get_channel(config['channels']['bank']):
            receivable_user = await ThornyFactory.build(user)
            payable_user = await ThornyFactory.build(ctx.author)

            if user == ctx.author:
                raise errors.SelfPaymentError
            elif payable_user.balance - amount < 0:
                raise errors.BrokeError
            elif amount > 0:
                payable_user.balance -= amount
                receivable_user.balance += amount

                pay_embed = discord.Embed(color=0xF4C430)
                pay_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
                pay_embed.add_field(name='<:Nug:884320353202081833> Payment Successful!',
                                    value=f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Paid to: **{user.mention}**\n'
                                          f'\n**Reason: {reason}**')
                await ctx.respond(f"{user.mention} You've been paid!")
                await ctx.edit(content=None, embed=pay_embed)

                event: ev.Event = await ev.fetch(ev.PlayerTransaction, payable_user, self.client)
                event.metadata.sender_user = payable_user
                event.metadata.receiver_user = receivable_user
                event.metadata.nugs_amount = amount
                event.metadata.event_comment = reason

                await event.log_event_in_discord()
                await commit(payable_user)
                await commit(receivable_user)
            elif amount < 0:
                raise errors.NegativeAmountError
        else:
            raise errors.ItemNotAvailableError

    treasury = discord.SlashCommandGroup("treasury", "Treasury Commands")

    @treasury.command(description="Store money in your kingdom's treasury")
    async def store(self, ctx, amount: int):
        user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        thorny_user = await ThornyFactory.build(user)
        thorny_user.kingdom = kingdom

        if kingdom is not None:
            selector = dbutils.Base()
            receivable = await selector.select("treasury", "kingdoms", "kingdom", kingdom)
            receivable = receivable[0][0]

            if thorny_user.balance - amount < 0:
                raise errors.BrokeError
            else:
                thorny_user.balance -= amount
                selector = dbutils.Base()
                await selector.update("treasury", receivable + int(amount), "kingdoms", "kingdom", kingdom)

                pay_embed = discord.Embed(color=0xE49B0F)
                pay_embed.set_author(name=f'{user}', icon_url=user.display_avatar.url)
                pay_embed.add_field(name='<:Nug:884320353202081833> Storage Successful!',
                                    value=f'Amount stored: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Stored in: **{kingdom} Treasury**\n')
                await ctx.respond(embed=pay_embed)
                await commit(thorny_user)
        else:
            raise errors.StoreError

    @treasury.command(description="Ruler Only | Take money from the treasury")
    @commands.has_role('Ruler')
    async def take(self, ctx, amount: int):
        user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        thorny_user = await ThornyFactory.build(user)
        thorny_user.kingdom = kingdom

        selector = dbutils.Base()
        payable = await selector.select("treasury", "kingdoms", "kingdom", kingdom)
        payable = payable[0][0]

        if amount < 0:
            raise errors.NegativeAmountError
        elif payable - amount < 0:
            raise errors.BrokeError
        else:
            thorny_user.balance += amount
            await selector.update("treasury", payable - int(amount), "kingdoms", "kingdom", kingdom)

            pay_embed = discord.Embed(color=0xE49B0F)
            pay_embed.set_author(name=f'{ctx.author}', icon_url=user.display_avatar.url)
            pay_embed.add_field(name='<:Nug:884320353202081833> Taking Successful!',
                                value=f'Amount taken: **<:Nug:884320353202081833>{amount}**\n'
                                      f'Taken from: **{kingdom} Treasury**\n')
            await ctx.respond(embed=pay_embed)
            await commit(thorny_user)
