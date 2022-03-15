import discord
from discord.ext import commands

import json
from thorny_code import dbutils
from thorny_code import errors
from thorny_code import logs
from thorny_code import functions as func


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, help='CM Only | Strike someone for bad behaviour')
    @commands.has_permissions(administrator=True)
    async def strike(self, ctx, user: discord.Member, *reason):
        strike_id = await dbutils.Profile.insert_strike(user.id, ' '.join(reason), ctx.author.id)
        strike_embed = discord.Embed(color=0xCD853F)
        strike_embed.add_field(name=f"**{user} Got Striked!**",
                               value=f"From: {ctx.author.mention}\n"
                                     f"Reason: {' '.join(reason)}")
        strike_embed.set_footer(text=f"Strike ID: {strike_id}")
        await ctx.send(embed=strike_embed)

    @strike.command(help='CM Only | Remove a strike')
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, strike_id):
        if await dbutils.Profile.delete_strike(int(strike_id)):
            await ctx.send(f"Strike {strike_id} has been removed")

    @commands.command(help='View a persons strikes')
    async def strikes(self, ctx, user: discord.Member):
        profile = json.load(open('./../thorny_data/profiles.json', 'r'))
        num = 0
        for strike in profile[str(user.id)]['strikes']:
            if strike != 'counter':
                strike = profile[str(user.id)]['strikes'][strike]
                if strike.get('disregarded') is not None:
                    pass
                else:
                    num += 1
                    await ctx.send(f"**Strike {num}** | ID: #{strike['id']}\n"
                                   f"Reason: {strike['reason']}\nFrom: {strike['CM']}")

    @commands.command(help='CM Only | Send someone to the Gulag')
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
            await ctx.send(f"{user.display_name} Has entered the Gulag! https://tenor.com/view/ba-sing-se-gif-20976912")
        else:
            await user.remove_roles(timeout_role)
            await user.add_roles(citizen_role)
            await ctx.send(f"{user.display_name} Has left the Gulag! https://tenor.com/view/ba-sing-se-gif-20976912")