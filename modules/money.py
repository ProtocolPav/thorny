import discord
from discord.ext import commands
from datetime import datetime

from thorny_core import thorny_errors
from thorny_core.uikit import embeds
import thorny_core.nexus as nexus


class Money(commands.Cog):
    def __init__(self, client):
        self.client = client

    balance = discord.SlashCommandGroup("balance", "Balance Commands")

    @balance.command(description="View someone's balance")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        thorny_user = await nexus.ThornyUser.build(user)
        thorny_guild = await nexus.ThornyGuild.build(user.guild)

        await ctx.respond(embed=embeds.balance_embed(thorny_user, thorny_guild))

    @balance.command(description="Edit someone's balance")
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx: discord.ApplicationContext, user: discord.Member,
                   amount: discord.Option(int, "Negative number to remove money")):
        thorny_user = await nexus.ThornyUser.build(user)
        thorny_guild = await nexus.ThornyGuild.build(user.guild)
        thorny_user.balance += amount

        await thorny_user.update()

        await ctx.respond(embed=embeds.balance_edit_embed(thorny_user, thorny_guild, amount),
                          ephemeral=True)

        if amount <= 0:
            transaction_type = "Remove Balance"
        else:
            transaction_type = "Add Balance"

        reason = f"{ctx.user.mention} edited {thorny_user.discord_member.mention}'s balance"

        if thorny_guild.get_channel_id('logs'):
            logs_channel = self.client.get_channel(thorny_guild.get_channel_id('logs'))
            await logs_channel.send(embed=embeds.transaction_log(thorny_user, thorny_guild,
                                                                 transaction_type, abs(amount),
                                                                 reason, datetime.now()))

    @commands.slash_command(description="Pay a player using money")
    async def pay(self, ctx: discord.ApplicationContext, user: discord.Member, amount: int, reason: str):
        receivable_user = await nexus.ThornyUser.build(user)
        thorny_user = await nexus.ThornyUser.build(ctx.user)
        thorny_guild = await nexus.ThornyGuild.build(user.guild)
        reason = f"[Payment] {reason}"

        if user == ctx.author:
            raise thorny_errors.SelfPaymentError
        elif thorny_user.balance - amount < 0:
            raise thorny_errors.BrokeError
        elif amount > 0:
            thorny_user.balance -= amount
            receivable_user.balance += amount

            await thorny_user.update()
            await receivable_user.update()

            await ctx.respond(content=f"{user.mention} You've been paid!",
                              embed=embeds.payment_embed(thorny_user, receivable_user, thorny_guild, amount, reason))

            if thorny_guild.get_channel_id('logs'):
                logs_channel = self.client.get_channel(thorny_guild.get_channel_id('logs'))
                await logs_channel.send(embed=embeds.transaction_log(thorny_user, thorny_guild,
                                                                     "Remove Balance", abs(amount),
                                                                     reason, datetime.now()))
                await logs_channel.send(embed=embeds.transaction_log(receivable_user, thorny_guild,
                                                                     "Add Balance", abs(amount),
                                                                     reason, datetime.now()))
        elif amount < 0:
            raise thorny_errors.NegativeAmountError
