import discord
from discord.ext import commands
from datetime import datetime

from thorny_core import errors
from thorny_core.db import UserFactory, commit, GuildFactory
from thorny_core.db import event
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

    @balance.command(description="Edit someone's balance")
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, user: discord.Member,
                   amount: discord.Option(int, "Negative number to remove money")):
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(user.guild)
        thorny_user.balance += amount

        if 'edit' in ctx.command.qualified_name.lower():
            await ctx.respond(embed=embeds.balance_edit_embed(thorny_user, thorny_guild, amount),
                              ephemeral=True)

        await commit(thorny_user)

    @commands.slash_command(description="Pay a player using money")
    async def pay(self, ctx, user: discord.Member, amount: int, reason: str):
        receivable_user = await UserFactory.build(user)
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(user.guild)

        if user == ctx.author:
            raise errors.SelfPaymentError
        elif thorny_user.balance - amount < 0:
            raise errors.BrokeError
        elif amount > 0:
            thorny_user.balance -= amount
            receivable_user.balance += amount

            await ctx.respond(f"{user.mention} You've been paid!")
            await ctx.edit(content=None, embed=embeds.payment_embed(thorny_user, receivable_user, thorny_guild, amount, reason))

            transaction = event.Transaction(self.client, datetime.now(), thorny_user, thorny_guild,
                                                receivable_user, amount, reason)

            await transaction.log()
            await commit(thorny_user)
            await commit(receivable_user)
        elif amount < 0:
            raise errors.NegativeAmountError

    @commands.slash_command(description="Work for some money")
    async def work(self, ctx: discord.ApplicationContext):
        thorny_guild = await GuildFactory.build(ctx.guild)
        GuildFactory.check_guild_feature(thorny_guild, 'BETA')

        await ctx.respond("Nothing happened...")
