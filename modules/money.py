import discord
from discord.ext import commands

import json
from thorny_core import errors
from thorny_core.db import UserFactory, commit, GuildFactory
from thorny_core import dbevent as ev
from thorny_core.uikit import embeds


class Money(commands.Cog):
    def __init__(self, client):
        self.client = client

    balance = discord.SlashCommandGroup("balance", "Balance Commands")

    @balance.command(description="View someone's balance")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(user.guild)

        await ctx.respond(embed=embeds.inventory_embed(thorny_user, thorny_guild))

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
            pay_embed.add_field(name=f'{thorny_guild.currency.emoji} Payment Successful!',
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
