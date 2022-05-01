import discord
from discord.ext import commands

from thorny_core import dbclass as db
from thorny_core.dbfactory import ThornyFactory
from thorny_core.dbcommit import commit


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description='CM Only | Strike someone for bad behaviour')
    @commands.has_permissions(administrator=True)
    async def strike(self, ctx, user: discord.Member, reason):
        thorny_user = await ThornyFactory.build(user)
        await thorny_user.strikes.append(ctx.author.id, reason)
        strike_embed = discord.Embed(color=0xCD853F)
        strike_embed.add_field(name=f"**{user} Got Striked!**",
                               value=f"From: {ctx.author.mention}\n"
                                     f"Reason: {reason}")
        strike_embed.set_footer(text=f"Strike ID: {thorny_user.strikes.strike_list[-1]['id']}")
        await ctx.respond(embed=strike_embed)
        await commit(thorny_user)

    @commands.slash_command(description='[DISABLED] CM Only | Remove a strike')
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, strike_id):
        await ctx.respond("Command is disabled")

    @commands.slash_command(description='[DISABLED] View a persons strikes')
    async def strikes(self, ctx, user: discord.Member):
        await ctx.respond("Command is disabled")

    @commands.slash_command(description='CM Only | Send someone to the Gulag')
    @commands.has_permissions(administrator=True)
    async def gulag(self, ctx, user: discord.Member):
        timeout_role = discord.utils.get(ctx.guild.roles, name="Time Out")
        citizen_role = discord.utils.get(ctx.guild.roles, name="Citizen")
        not_playing_role = discord.utils.get(ctx.guild.roles, name="Not Playing")
        if timeout_role not in user.roles:
            if citizen_role in user.roles:
                await user.remove_roles(citizen_role)
            elif not_playing_role in user.roles:
                await user.remove_roles(not_playing_role)
            await user.add_roles(timeout_role)
            await ctx.respond(f"{user.display_name} Has entered the Gulag! "
                              f"https://tenor.com/view/ba-sing-se-gif-20976912")
        else:
            await user.remove_roles(timeout_role)
            await user.add_roles(citizen_role)
            await ctx.respond(f"{user.display_name} Has left the Gulag! "
                              f"https://tenor.com/view/ba-sing-se-gif-20976912")
