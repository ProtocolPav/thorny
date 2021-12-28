import discord
from discord.ext import commands

import json
import errors
import logs
import functions as func

config = json.load(open("./../thorny_data/config.json", "r"))


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, help='CM Only | Strike someone for bad behaviour')
    @commands.has_permissions(administrator=True)
    async def strike(self, ctx, user: discord.Member, *reason):
        func.profile_update(user)
        file_counters = open('./../thorny_data/counters.json', 'r+')
        counters = json.load(file_counters)
        counters['strike_id'] += 1
        file_counters.truncate(0)
        file_counters.seek(0)
        json.dump(counters, file_counters)
        strike = {"CM": f"{ctx.author}",
                  "reason": " ".join(reason),
                  "id": counters['strike_id']}

        profile = json.load(open('./../thorny_data/profiles.json', 'r'))
        func.profile_update(user, strike, 'strikes', f"strike_{len(profile[f'{user.id}']['strikes']) + 1}")
        func.profile_update(user, profile[str(user.id)]['strikes']['counter'] + 1, 'strikes', 'counter')
        strike_embed = discord.Embed(color=0xCD853F)
        strike_embed.add_field(name=f"**{user} Got Striked!**",
                               value=f"This is **Strike Number {profile[str(user.id)]['strikes']['counter'] + 1}!**\n"
                                     f"From: {ctx.author.mention}\n"
                                     f"Reason: {' '.join(reason)}")
        strike_embed.set_footer(text=f"Strike ID: {counters['strike_id']}")
        await ctx.send(embed=strike_embed)

    @strike.command(help='CM Only | Remove a strike')
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member, strike_id, *reason):
        profile = json.load(open('./../thorny_data/profiles.json', 'r'))
        strike = profile[f'{user.id}']['strikes'][f'strike_{strike_id}']
        strike['disregarded'] = True
        strike['disregard_reason'] = " ".join(reason)
        func.profile_update(user, strike, 'strikes', f"strike_{strike_id}")
        func.profile_update(user, profile[str(user.id)]['strikes']['counter'] - 1, 'strikes', 'counter')
        await ctx.send(f"{user}'s Strike {strike_id} has been disregarded for {' '.join(reason)}!")

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
            await ctx.send(f"{user.display_name} Has entered the Gulag!")
            stafflogs = self.client.get_channel(config['channels']['event_logs'])
            await stafflogs.send(embed=logs.gulag(ctx.author.id, user.id))
            gulag = self.client.get_channel(config['channels']['gulag_channel'])
            await gulag.send("**Welcome To The Gulag.**\nhttps://tenor.com/view/ba-sing-se-gif-20976912")
        else:
            await user.remove_roles(timeout_role)
            await user.add_roles(citizen_role)
            await ctx.send(f"{user.display_name} Has left the Gulag!")