import discord
from discord.ext import commands

import json
import errors
import functions as func


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def strike(self, ctx, user: discord.Member, *reason):
        func.profile_update(user)
        strike = {"CM": f"{ctx.author}",
                  "reason": " ".join(reason)}

        profile = json.load(open('./../thorny_data/profiles.json', 'r'))
        func.profile_update(user, strike, 'strikes', f"strike_{len(profile[f'{user.id}']['strikes']) + 1}")
        strike_embed = discord.Embed(color=0xCD853F)
        strike_embed.add_field(name=f"**{user} Got Striked!**",
                               value=f"This is **Strike Number {len(profile[str(user.id)]['strikes']) + 1}!**\n"
                                     f"From: {ctx.author}\n"
                                     f"Reason: {' '.join(reason)}")
        await ctx.send(embed=strike_embed)

    @strike.command(aliases=['disregard'])
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, strike_id, user: discord.Member, *reason):
        profile = json.load(open('./../thorny_data/profiles.json', 'r'))
        strike = profile[f'{user.id}']['strikes'][f'strike_{strike_id}']
        strike['disregarded'] = True
        strike['disregard_reason'] = " ".join(reason)
        func.profile_update(user, strike, 'strikes', f"strike_{strike_id}")
        await ctx.send(f"{user}'s Strike {strike_id} has been disregarded for {' '.join(reason)}!")

    @strike.command()
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx):
        pass
