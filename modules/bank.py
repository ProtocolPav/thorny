import discord
from discord.ext import commands

import json
from thorny_core import errors
from thorny_core.db import UserFactory, commit, GuildFactory
from thorny_core import dbevent as ev


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    balance = discord.SlashCommandGroup("balance", "Balance Commands")

    @balance.command(description="View someone's balance")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(user.guild)

        personal_bal = f"**Personal Balance:** {thorny_guild.currency.emoji}{thorny_user.balance}"
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
                                value=f"{personal_bal}")
        balance_embed.add_field(name=f'**Inventory:**',
                                value=f"{inventory_text}<:_purple:921708790368309269> "
                                      f"**/inventory view to see more!**",
                                inline=False)
        balance_embed.set_footer(text="You can pay people! Just use /pay")
        await ctx.respond(embed=balance_embed)

    @balance.command(description="CM ONLY | Edit someone's balance")
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, user: discord.Member,
                   amount: discord.Option(int, "Put a - if you want to remove currency")):
        thorny_user = await UserFactory.build(user)
        thorny_user.balance += amount

        if 'edit' in ctx.command.qualified_name.lower():
            await ctx.respond(f"{user}'s balance is now **{thorny_user.balance}**! (Added/Removed: {amount})")
        await commit(thorny_user)

    @commands.slash_command(description="Pay a player using nugs")
    async def pay(self, ctx, user: discord.Member, amount: int, reason: str):
        receivable_user = await UserFactory.build(user)
        payable_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(user.guild)

        if user == ctx.author:
            raise errors.SelfPaymentError
        elif payable_user.balance - amount < 0:
            raise errors.BrokeError
        elif amount > 0:
            payable_user.balance -= amount
            receivable_user.balance += amount

            pay_embed = discord.Embed(color=0xF4C430)
            pay_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            pay_embed.add_field(name='{thorny_guild.currency.emoji} Payment Successful!',
                                value=f'Amount paid: **{thorny_guild.currency.emoji}{amount}**\n'
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
