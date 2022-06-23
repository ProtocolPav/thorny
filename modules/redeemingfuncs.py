import asyncio
import discord
from discord.ext import commands

import json
from thorny_core import functions as func
from thorny_core import errors
import random
from thorny_core import dbutils
from thorny_core.dbclass import ThornyUser
from thorny_core.dbfactory import ThornyFactory
from thorny_core.dbcommit import commit
from discord import utils
from datetime import datetime, timedelta
from thorny_core import dbevent as ev


async def redeem_ticket(ctx, thorny_user: ThornyUser):
    ticket_prizes = [[":yellow_heart:", 1], [":gem:", 2], [":dagger:", 4], ["<:grassyE:840170557508026368>", 6],
                     ["<:goldenE:857714717153689610>", 7], [":dragon_face:", 64]]

    able_to_redeem = True
    if random.choices([True, False], weights=(2, 98), k=1)[0]:
        raise errors.FaultyTicketError()
    else:
        prizes = []
        winnings = []
        for i in range(4):
            random_icon = random.choices(ticket_prizes, weights=(2.99, 4, 5, 3, 1, 0.01), k=1)
            prizes.append(random_icon[0])
            winnings.append(f"||{random_icon[0][0]}||")

        selector = dbutils.Base()
        counter = await selector.select("count", "counter", "counter_name", "ticket_count")
        ticket_embed = discord.Embed(color=ctx.author.color)
        ticket_embed.add_field(name="**Scratch Ticket**",
                               value=f"Scratch your ticket and see your prize!\n{' '.join(winnings)}")
        ticket_embed.set_footer(text=f"Ticket #{counter[0][0] + 1} "
                                     f"| Use /tickets to see how Prizes work!")
        if thorny_user.counters.ticket_count >= 4:
            if datetime.now() - thorny_user.counters.ticket_last_purchase <= timedelta(hours=23):
                time = datetime.now() - thorny_user.counters.ticket_last_purchase
                able_to_redeem = False
                thorny_user.inventory.add_item("ticket", 1)
                await ctx.respond(f"You already redeemed 4 tickets! Next time you can redeem is in "
                                  f"{timedelta(hours=23) - time}")
            else:
                thorny_user.counters.ticket_count = 0
        if able_to_redeem:
            await ctx.respond(embed=ticket_embed)
            thorny_user.balance += thorny_user.calculate_ticket_reward(prizes, ticket_prizes)
            thorny_user.counters.ticket_count += 1
            thorny_user.counters.ticket_last_purchase = datetime.now().replace(microsecond=0)


async def redeem_role(ctx, thorny_user: ThornyUser, client):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    customization_embed = discord.Embed(color=ctx.author.color)
    customization_embed.add_field(name="**You have redeemed a Custom Role for 1 Month!**",
                                  value=f"Congrats on your sweet new role! Now it's time to customize it.\n"
                                        f"What name do you want your custom role to have?\nPlease don't"
                                        f" make it too long, discord has limitations too!")
    customization_embed.set_footer(text="Customization 1/2 | 60 seconds left to reply")

    customization2_embed = discord.Embed(color=ctx.author.color)
    customization2_embed.add_field(name="**You have redeemed a Custom Role for 1 Month!**",
                                   value="Nice! That sounds like a great role name!"
                                         f"\nNow, what colour? Please use a `#hex code` with the #")
    customization2_embed.set_footer(text="Customization 2/2 | 60 seconds left to reply")
    try:
        await ctx.respond(embed=customization_embed)
        name = await client.wait_for('message', check=check, timeout=60.0)
        role_name = name.content.capitalize()

        await ctx.respond(embed=customization2_embed)
        colour = await client.wait_for('message', check=check, timeout=60.0)
        if '#' in colour.content:
            role = await ctx.guild.create_role(name=role_name,
                                               color=int(f'0x{colour.content[1:7]}', 16))
            await role.edit(position=discord.utils.get(ctx.guild.roles,
                                                       name="Donator").position)
            await ctx.author.add_roles(role)

            customization3_embed = discord.Embed(color=int(f'0x{colour.content[1:7]}', 16))
            customization3_embed.add_field(name="**You have redeemed a Custom Role for 1 Month!**",
                                           value=f"Done! {role_name} has been added to your roles!")
            customization3_embed.set_footer(text="Complete! | roleredeem")
            await ctx.respond(embed=customization3_embed)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to answer! Use `/redeem role` again to restart")
        thorny_user.inventory.add_item("role", 1)
