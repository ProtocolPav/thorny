import asyncio

import discord
from discord.ext import commands
import json
from functions import profile_update, calculate_prizes
import functions as func
import errors
import logs
import random
from datetime import datetime, timedelta
from modules import bank
import dbutils
from discord import utils

config = json.load(open("./../thorny_data/config.json", "r"))
vers = json.load(open('version.json', 'r'))
v = vers["version"]


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def get_items(ctx):
        item_types = await dbutils.simple_select('item_type', '*')
        list = []
        for item in item_types:
            list.append(item['friendly_id'])
        return list

    inventory = discord.SlashCommandGroup("inventory", "Inventory Commands")

    @inventory.command(aliases=['inv'], invoke_without_command=True, help="See you or a person's Inventory")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        await dbutils.simple_update('user', 'kingdom', kingdom, 'user_id', user.id)

        balance_list = await dbutils.condition_select("user", "balance", "user_id", user.id)
        personal_bal = f"**Personal Balance:** <:Nug:884320353202081833>{balance_list[0][0]}"
        kingdom_bal = ''
        if kingdom is not None:
            treasury_list = await dbutils.condition_select("kingdoms", 'treasury', 'kingdom', kingdom)
            kingdom_bal = f"**{kingdom.capitalize()} Treasury:** <:Nug:884320353202081833>" \
                          f"{treasury_list[0][0]}"
        inventory_text = ''
        inventory_list = await dbutils.condition_select("inventory", "*", "user_id", user.id)
        for item in inventory_list:
            item_type = await dbutils.Inventory.get_item_type(item['item_id'])
            inventory_text = f'{inventory_text}<:_pink:921708790322192396> ' \
                             f'{item["item_count"]} **|** {item_type["display_name"]}\n'
        if len(inventory_list) < 9:
            for item in range(0, 9 - len(inventory_list)):
                inventory_text = f'{inventory_text}<:_pink:921708790322192396> Empty\n'

        inventory_embed = discord.Embed(colour=0xE0115F)
        inventory_embed.set_author(name=user, icon_url=user.avatar)
        inventory_embed.add_field(name=f'**Financials:**', value=f"{personal_bal}\n{kingdom_bal}")
        inventory_embed.add_field(name=f"**Inventory**", value=inventory_text, inline=False)
        inventory_embed.set_footer(text="Use /redeem <item_id> to redeem Roles & Tickets!")
        await ctx.respond(embed=inventory_embed)

    @inventory.command(hidden=True, help="Add an item to a user's inventory")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.Member = None,
                  item_id: discord.Option(str, "Select an item to redeem",
                                          autocomplete=utils.basic_autocomplete(get_items)) = None, count=1):
        item_data = await dbutils.Inventory.get_item_type(item_id)
        inv_item = await dbutils.Inventory.select(item_data['friendly_id'], user.id)
        item_added = True
        if not item_data:
            await ctx.send("Wrong Inventory")
            item_added = False
        elif inv_item and inv_item['item_count'] + int(count) <= item_data['max_item_count']:
            await dbutils.Inventory.update(item_data['friendly_id'], inv_item['item_count'] + int(count), user.id)
        elif not inv_item and int(count) <= item_data['max_item_count']:
            await dbutils.Inventory.insert(item_data['friendly_id'], int(count), user)
        else:
            if 'add' in ctx.command.qualified_name.lower():
                await ctx.respond(f"You are adding too many! Max count for this item is {item_data['max_item_count']}")
            elif 'buy' in ctx.command.qualified_name.lower():
                await ctx.respond(
                    f"You can't buy any more! Max amount you can have is **{item_data['max_item_count']}**")
            item_added = False

        if item_added and 'add' in ctx.command.qualified_name.lower():
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Inventory Added Successfully**",
                                     value=f"Added {count}x `{item_data['display_name']}` to {user}'s Inventory")
            await ctx.respond(embed=inv_edit_embed)
        elif item_added and 'buy' in ctx.command.qualified_name.lower():
            return item_added

    @inventory.command(hidden=True, help="Remove or clear and item from a user's inventory")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member = None,
                     item_id: discord.Option(str, "Select an item to redeem",
                                             autocomplete=utils.basic_autocomplete(get_items)) = None, count=None):
        item_data = await dbutils.Inventory.get_item_type(item_id)
        inv_item = await dbutils.Inventory.select(item_data['friendly_id'], user.id)
        item_removed = True
        if not item_data:
            await ctx.send("Wrong Inventory")
            item_removed = False
        elif inv_item:
            if count is None or inv_item['item_count'] - int(count) <= 0:
                await dbutils.Inventory.delete(item_data['friendly_id'], user.id)
                count = inv_item['item_count']
            else:
                await dbutils.Inventory.update(item_data['friendly_id'], inv_item['item_count'] - int(count), user.id)
        else:
            await ctx.respond(embed=errors.Inventory.item_missing_error, ephemeral=True)
            item_removed = False

        if item_removed and 'remove' in ctx.command.qualified_name.lower():
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Inventory Removed Successfully**",
                                     value=f"Removed {count}x `{item_data['display_name']}` "
                                           f"from {user}'s Inventory")
            await ctx.respond(embed=inv_edit_embed)
        elif item_removed and 'redeem' in ctx.command.qualified_name.lower():
            return item_removed

    store = discord.SlashCommandGroup("store", "Store Commands")

    @store.command(invoke_without_command=True, help="Get a list of all items available in the store")
    async def catalogue(self, ctx):
        item_types = await dbutils.simple_select('item_type', '*')
        store_embed = discord.Embed(colour=ctx.author.colour)
        item_text = ""
        for item in item_types:
            if item['item_cost'] > 0:
                item_text = f"{item_text}\n**{item['display_name']}** |" \
                            f" <:Nug:884320353202081833>{item['item_cost']}\n" \
                            f"**Item ID:** {item['friendly_id']}\n"
        store_embed.add_field(name=f'**Items Available:**',
                              value=f"{item_text}", inline=False)
        store_embed.set_footer(text=f"{v} | Use !store buy <item_id> to purchase!")
        await ctx.respond(embed=store_embed)

    @store.command(help="Purchase an item from the store", brief='!store buy ticket')
    async def buy(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                     autocomplete=utils.basic_autocomplete(get_items)), amount=1):
        item_type = await dbutils.Inventory.get_item_type(item_id)
        balance = await dbutils.condition_select('user', 'balance', 'user_id', ctx.author.id)

        if item_type and balance[0][0] - item_type['item_cost'] * amount >= 0 and item_type['item_cost'] != 0:
            await dbutils.simple_update('user', 'balance', balance[0][0] - item_type['item_cost'] * amount,
                                        'user_id', ctx.author.id)
            if await Inventory.add(self, ctx, ctx.author, item_type['friendly_id'], amount):
                inv_edit_embed = discord.Embed(colour=ctx.author.colour)
                inv_edit_embed.add_field(name="**Cha-Ching!**",
                                         value=f"Bought {amount}x `{item_type['display_name']}`")
                inv_edit_embed.set_footer(text=f"{v} | Use !redeem <item_id> to redeem")
                await ctx.respond(embed=inv_edit_embed)
                bank_log = self.client.get_channel(config['channels']['bank_logs'])
                await bank_log.send(embed=logs.transaction(ctx.author.id, 'Store',
                                                           item_type['item_cost'] * amount, ['Scratch Ticket']))
        elif balance[0][0] - item_type['item_cost'] * amount < 0:
            await ctx.respond(embed=errors.Pay.lack_nugs_error, ephemeral=True)
        elif not item_type or item_type['item_cost'] == 0:
            await ctx.respond(embed=errors.Shop.item_error, ephemeral=True)

    @store.command(help="Edit Prices of tickets", hidden=True)
    @commands.has_permissions(administrator=True)
    async def price(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                       autocomplete=utils.basic_autocomplete(get_items)), price):
        if await dbutils.Inventory.update_item_price(item_id, price):
            await ctx.respond(f"Done! {item_id} is now {price} Nugs", ephemeral=True)

    @commands.slash_command(help="Redeem an item from your inventory. Items: ticket, role, gift", brief='!redeem role')
    async def redeem(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                        autocomplete=utils.basic_autocomplete(get_items))):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        redeemable_id = [1, 2, 4]
        ticket_prizes = [[":yellow_heart:", 1], [":gem:", 2], [":dagger:", 4], ["<:grassyE:840170557508026368>", 6],
                         ["<:goldenE:857714717153689610>", 7], [":dragon_face:", 64]]

        item_type = await dbutils.Inventory.get_item_type(item_id)
        if item_type['unique_id'] in redeemable_id:
            removed = await Inventory.remove(self, ctx, ctx.author, item_id, 1)

            if removed and item_type['unique_id'] == 1:
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
                    name = await self.client.wait_for('message', check=check, timeout=60.0)
                    role_name = name.content.capitalize()

                    await ctx.respond(embed=customization2_embed)
                    colour = await self.client.wait_for('message', check=check, timeout=60.0)
                    if '#' in colour.content:
                        role = await ctx.guild.create_role(name=role_name,
                                                           color=int(f'0x{colour.content[1:7]}', 16))
                        await role.edit(position=discord.utils.get(ctx.guild.roles,
                                                                   name="Donator").position)
                        await ctx.author.add_roles(role)

                        customization3_embed = discord.Embed(color=int(f'0x{colour.content[1:7]}', 16))
                        customization3_embed.add_field(name="**You have redeemed a Custom Role for 1 Month!**",
                                                       value=f"Done! {role_name} has been added to your roles!")
                        customization3_embed.set_footer(text="Complete!")
                        await ctx.respond(embed=customization3_embed)
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to answer! Use `!redeem role` again to restart")
                    await Inventory.add(self, ctx, ctx.author, item_id, 1)

            elif removed and item_type['unique_id'] == 2:
                if random.choices([True, False], weights=(2, 98), k=1)[0]:
                    await ctx.respond(embed=errors.Shop.faulty_ticket_error)
                else:
                    prizes = []
                    winnings = []
                    for i in range(4):
                        random_icon = random.choices(ticket_prizes, weights=(2.98, 4, 5, 3, 1, 0.01), k=1)
                        prizes.append(random_icon[0])
                        winnings.append(f"||{random_icon[0][0]}||")

                    counter = await dbutils.condition_select('counter', 'count', 'counter_name', 'ticket_count')
                    ticket_embed = discord.Embed(color=ctx.author.color)
                    ticket_embed.add_field(name="**Scratch Ticket**",
                                           value=f"Scratch your ticket and see your prize!\n{' '.join(winnings)}")
                    ticket_embed.set_footer(text=f"Ticket #{counter[0][0] + 1} "
                                                 f"| Use !tickets to see how Prizes work!")
                    await ctx.respond(embed=ticket_embed)
                    bal = await dbutils.condition_select("user", "balance", "user_id", ctx.author.id)
                    await dbutils.simple_update('user', 'balance',
                                                bal[0][0] + func.calculate_prizes(prizes, ticket_prizes),
                                                'user_id', ctx.author.id)
                    await dbutils.simple_update('counter', 'count', counter[0][0] + 1, 'counter_name', 'ticket_count')
        else:
            await ctx.respond("Wrong item!")

    @commands.command(help="See how tickets work!")
    async def tickets(self, ctx):
        help_embed = discord.Embed(color=ctx.author.color)
        help_embed.add_field(name="**How Prizes Work**",
                             value="There are 2 types of prizes:\n\n"
                                   "**Normal Prize**\n"
                                   ":yellow_heart: - 1 nug, :gem: - 2 nugs, :dagger: - 4 nugs, "
                                   "<:grassyE:840170557508026368> - 6 nugs, <:goldenE:857714717153689610> - 7 nugs, "
                                   ":dragon_face: - 64 nugs\n\n"
                                   "**Jackpot Prize**\n"
                                   "When you get 4 different scratchables, you get double the prize! Except for when "
                                   "you get a :dragon_face:.\n\n"
                                   "Nugs are added automatically!", inline=False)
        await ctx.send(embed=help_embed)
