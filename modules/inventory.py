import asyncio
import discord
from discord.ext import commands

import json
from thorny_core import functions as func
from thorny_core import errors
import random
from thorny_core import dbutils
from thorny_core.dbfactory import ThornyFactory
from thorny_core.dbcommit import commit
from discord import utils
from datetime import datetime, timedelta
from thorny_core import dbevent as ev

config = json.load(open("./../thorny_data/config.json", "r"))
vers = json.load(open('version.json', 'r'))
v = vers["version"]


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def get_items(ctx):
        selector = dbutils.Base()
        item_types = await selector.select("*", "item_type")
        item_list = []
        for item in item_types:
            item_list.append(item['friendly_id'])
        return item_list

    inventory = discord.SlashCommandGroup("inventory", "Inventory Commands")

    @inventory.command(description="See you or a person's Inventory")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        kingdom = func.get_user_kingdom(ctx, user)
        thorny_user = await ThornyFactory.build(user)
        thorny_user.kingdom = kingdom
        await commit(thorny_user)

        personal_bal = f"**Personal Balance:** <:Nug:884320353202081833>{thorny_user.balance}"
        kingdom_bal = ''
        if kingdom is not None:
            selector = dbutils.Base()
            treasury_list = await selector.select("treasury", "kingdoms", "kingdom", kingdom)
            kingdom_bal = f"**{kingdom.capitalize()} Treasury:** <:Nug:884320353202081833>" \
                          f"{treasury_list[0][0]}"
        inventory_text = ''
        inventory_list = thorny_user.inventory.slots
        for item in inventory_list:
            inventory_text = f'{inventory_text}<:_pink:921708790322192396> ' \
                             f'{item.item_count} **|** {item.item_display_name}\n'
        if len(inventory_list) < 9:
            for item in range(0, 9 - len(inventory_list)):
                inventory_text = f'{inventory_text}<:_pink:921708790322192396> Empty\n'

        inventory_embed = discord.Embed(colour=0xE0115F)
        inventory_embed.set_author(name=user, icon_url=user.display_avatar.url)
        inventory_embed.add_field(name=f'**Financials:**', value=f"{personal_bal}\n{kingdom_bal}")
        inventory_embed.add_field(name=f"**Inventory**", value=inventory_text, inline=False)
        inventory_embed.set_footer(text="Use /redeem to redeem Roles & Tickets!")
        await ctx.respond(embed=inventory_embed)

    store = discord.SlashCommandGroup("store", "Store Commands")

    @store.command(description="Get a list of all items available in the store")
    async def catalogue(self, ctx):
        selector = dbutils.Base()
        item_types = await selector.select("*", "item_type")
        store_embed = discord.Embed(colour=ctx.author.colour)
        item_text = ""
        for item in item_types:
            if item['item_cost'] > 0:
                item_text = f"{item_text}\n**{item['display_name']}** |" \
                            f" <:Nug:884320353202081833>{item['item_cost']}\n" \
                            f"**Item ID:** {item['friendly_id']}\n"
        store_embed.add_field(name=f'**Items Available:**',
                              value=f"{item_text}", inline=False)
        store_embed.set_footer(text=f"{v} | Use /store buy <item_id> to purchase!")
        await ctx.respond(embed=store_embed)

    @store.command(description="Purchase an item from the store")
    async def buy(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                     autocomplete=utils.basic_autocomplete(get_items)),
                  amount: int = 1):
        thorny_user = await ThornyFactory.build(ctx.author)
        item = None

        for item_data in thorny_user.inventory.all_item_metadata:
            if item_data['friendly_id'] == item_id:
                item = item_data

        if item["item_cost"] != 0 and thorny_user.balance - item["item_cost"] * amount >= 0:
            if await Inventory.add(self, ctx, ctx.author, item_id, amount):
                thorny_user.balance -= item['item_cost'] * amount
                inv_edit_embed = discord.Embed(colour=ctx.author.colour)
                inv_edit_embed.add_field(name="**Cha-Ching!**",
                                         value=f"Bought {amount}x `{item['display_name']}`")
                inv_edit_embed.set_footer(text=f"{v} | Use /redeem to redeem this item!")
                await ctx.respond(embed=inv_edit_embed)
                event: ev.StoreTransaction = await ev.fetch(ev.StoreTransaction, thorny_user, self.client)
                event.metadata.nugs_amount = item['item_cost'] * amount
                event.metadata.sender_user = ctx.author
                event.metadata.event_comment = f"Purchase of {amount}x {item['display_name']}"
                await event.log_event_in_discord()
        elif thorny_user.balance - item['item_cost'] * amount < 0:
            await ctx.respond(embed=errors.Pay.lack_nugs_error, ephemeral=True)
        elif item['item_cost'] == 0:
            await ctx.respond(embed=errors.Shop.item_error, ephemeral=True)
        await commit(thorny_user)

    @commands.slash_command(description="Redeem an item from your inventory")
    async def redeem(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                        autocomplete=utils.basic_autocomplete(get_items))):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        redeemable_id = ['role', 'ticket', 'gift']
        ticket_prizes = [[":yellow_heart:", 1], [":gem:", 2], [":dagger:", 4], ["<:grassyE:840170557508026368>", 6],
                         ["<:goldenE:857714717153689610>", 7], [":dragon_face:", 64]]

        thorny_user = await ThornyFactory.build(ctx.author)
        item = thorny_user.inventory.fetch(item_id)

        if item.item_id in redeemable_id:
            removed = await Inventory.remove(self, ctx, ctx.author, item.item_id, 1)

            if removed and item.item_id == 'role':
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
                        customization3_embed.set_footer(text="Complete! | roleredeem")
                        await ctx.respond(embed=customization3_embed)
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to answer! Use `/redeem role` again to restart")
                    await Inventory.add(self, ctx, ctx.author, item.item_id, 1)

            elif removed and item.item_id == 'ticket':
                able_to_redeem = True
                if random.choices([True, False], weights=(2, 98), k=1)[0]:
                    await ctx.respond(embed=errors.Shop.faulty_ticket_error)
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
                            await Inventory.add(self, ctx, ctx.author, item.item_id, 1)
                            await ctx.respond(f"You already redeemed 4 tickets! Next time you can redeem is in "
                                              f"{timedelta(hours=23) - time}")
                        else:
                            await thorny_user.counters.update("ticket_count", 0)
                    if able_to_redeem:
                        await ctx.respond(embed=ticket_embed)
                        thorny_user.balance += thorny_user.calculate_ticket_reward(prizes, ticket_prizes)
                        thorny_user.counters.ticket_count += 1
                        thorny_user.counters.ticket_last_purchase = datetime.now().replace(microsecond=0)
        elif item.item_id is None:
            await ctx.respond(embed=errors.Shop.empty_inventory_error)
        else:
            await ctx.respond(embed=errors.Shop.item_error)

    @commands.slash_command(description="See how tickets work!")
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
        await ctx.respond(embed=help_embed, ephemeral=True)
