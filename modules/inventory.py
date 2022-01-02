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

config = json.load(open("./../thorny_data/config.json", "r"))


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['inv'], invoke_without_command=True, help="See you or a person's Inventory")
    async def inventory(self, ctx, user: discord.Member = None):
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
            item_data = await dbutils.Inventory.get_item_type(item['item_id'])
            inventory_text = f'{inventory_text}<:_pink:921708790322192396> ' \
                             f'{item["item_count"]} **|** {item_data["display_name"]}\n'
        if len(inventory_list) < 9:
            for item in range(0, 9 - len(inventory_list)):
                inventory_text = f'{inventory_text}<:_pink:921708790322192396> 0 **|** Empty Slot\n'

        inventory_embed = discord.Embed(colour=0xE0115F)
        inventory_embed.set_author(name=user, icon_url=user.avatar_url)
        inventory_embed.add_field(name=f'**Financials:**', value=f"{personal_bal}\n{kingdom_bal}")
        inventory_embed.add_field(name=f"**Inventory**", value=inventory_text, inline=False)
        inventory_embed.set_footer(text="Use !redeem <item> to redeem Roles & Tickets!")
        await ctx.send(embed=inventory_embed)

    @inventory.command(hidden=True, help="Add items to a player's inventory.")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.User = None, item=None, count=1):
        item_data = await dbutils.Inventory.get_item_type(item)
        inv_item = await dbutils.Inventory.select(item_data['item_id'], user.id)
        item_added = True
        if not item_data:
            await ctx.send("Wrong Item")
            item_added = False
        elif inv_item:
            await dbutils.Inventory.update(item_data['item_id'], inv_item['item_count'] + count, user.id)
        else:
            await dbutils.Inventory.insert(item_data['item_id'], count, user.id)

        if item_added is True:
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Item Added Successfully**",
                                     value=f"Added {count}x `{item_data['display_name']}` to {user}'s Inventory")
            await ctx.send(embed=inv_edit_embed)

    @inventory.command(hidden=True, help="Remove items from player's inventory.")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.User = None, item=None, count=None):
        item_data = await dbutils.Inventory.get_item_type(item)
        inv_item = await dbutils.Inventory.select(item_data['item_id'], user.id)
        item_removed = True
        if not item_data:
            await ctx.send("Wrong Item")
            item_removed = False
        elif inv_item:
            if count is None:
                await dbutils.Inventory.delete(item_data['item_id'], user.id)
                count = inv_item['item_count']
            else:
                await dbutils.Inventory.update(item_data['item_id'], inv_item['item_count'] - count, user.id)
        else:
            await ctx.send(embed=errors.Inventory.item_missing_error)

        if item_removed is True:
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Item Removed Successfully**",
                                     value=f"Removed {count}x `{item_data[0]['display_name']}` "
                                           f"from {user}'s Inventory")
            await ctx.send(embed=inv_edit_embed)

    @commands.group(invoke_without_command=True, help="Get a list of all items available in the store")
    async def store(self, ctx):
        await ctx.send('Items in the Store:\n'
                       f'Ticket - {counters["ticket_price"]} nugs\n'
                       'Use `!store buy <item>` to buy an item!')

    @store.command(help="Purchase an item from the store. Items: Ticket")
    async def buy(self, ctx, item):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        counters = json.load(open('../thorny_data/counters.json', 'r+'))
        item_found = False
        slot = 0

        if item.lower() in 'scratch ticket':
            if profile[f'{ctx.author.id}']['balance'] - counters["ticket_price"] >= 0:
                new_balance = profile[f"{ctx.author.id}"]['balance'] - counters["ticket_price"]
                profile_update(ctx.author, new_balance, 'balance')
                while not item_found:
                    if slot <= 8:
                        slot += 1
                        item_id = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['item_id']
                        if item_id == "ticket_02":
                            amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['amount'] + 1
                            updated_slot = {'item_id': "ticket_02", "amount": amnt}
                            profile_update(ctx.author, updated_slot, 'inventory', f'slot{slot}')
                            item_found = True
                            await ctx.send(f"Bought a Ticket! Use `!redeem ticket` to redeem")
                    else:
                        for i in range(1, 10):
                            item_id = profile[f"{ctx.author.id}"]['inventory'][f'slot{i}']['item_id']
                            if item_id == "empty_00" and not item_found:
                                amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{i}']['amount'] + 1
                                updated_slot = {'item_id': "ticket_02", "amount": amnt}
                                profile_update(ctx.author, updated_slot, 'inventory', f'slot{i}')
                                item_found = True
                                await ctx.send(f"Bought a Ticket! Use `!redeem ticket` to redeem")
                bank_log = self.client.get_channel(config['channels']['bank_logs'])
                await bank_log.send(embed=logs.transaction(ctx.author.id, 'Store',
                                                           counters["ticket_price"], ['Scratch Ticket']))
            else:
                await ctx.send(embed=errors.Pay.lack_nugs_error)
        else:
            await ctx.send(embed=errors.Shop.item_error)

    @store.command(help="Edit Prices of tickets", hidden=True)
    async def edit(self, ctx, price):
        file_counters = open('../thorny_data/counters.json', 'r+')
        counters = json.load(file_counters)
        counters['ticket_price'] = int(price)
        file_counters.truncate(0)
        file_counters.seek(0)
        json.dump(counters, file_counters)
        file_counters.close()
        await ctx.send(f"Ticket Price set to {price}")

    @commands.command(help="Redeem an item from your inventory. Items: Ticket, Role")
    async def redeem(self, ctx, item):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_found = False
        slot = 0
        ticket_prizes = [[":gem:", 2], [":ringed_planet:", 3], [":tangerine:", 4], ["<:grassyE:840170557508026368>", 7],
                         ["<:goldenE:857714717153689610>", 15], [":heart_on_fire:", 30]]
        present_choices = ['role_01;1', 'ticket_02;1', 'nugs;13', 'nugs;24', 'ticket_02;4', 'coal;1', 'present_03;3']

        if item.lower() in 'scratch ticket':
            while not item_found:
                if slot <= 8:
                    slot += 1
                    item_id = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['item_id']
                    if item_id == "ticket_02":
                        amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['amount'] - 1
                        if amnt == 0:
                            updated_slot = {'item_id': "empty_00", "amount": 0}
                        else:
                            updated_slot = {'item_id': "ticket_02", "amount": amnt}
                        profile_update(ctx.author, updated_slot, 'inventory', f'slot{slot}')
                        item_found = True
                        if random.randint(0, 7) == 5:
                            await ctx.send(embed=errors.Shop.faulty_ticket_error)
                        else:
                            player_winnings = ""
                            player_prizes = []
                            for i in range(5):
                                random_icon = random.choices(ticket_prizes, weights=(8.9, 4.9, 3, 2, 1, 0.2), k=1)
                                player_winnings = f"{player_winnings} ||{random_icon[0][0]}||"
                                player_prizes.append(random_icon[0])
                            file_counters = open('./../thorny_data/counters.json', 'r+')
                            counters = json.load(file_counters)
                            ticket_embed = discord.Embed(color=ctx.author.color)
                            ticket_embed.add_field(name="**Scratch Ticket**",
                                                   value=f"Scratch your ticket and see your prize!\n{player_winnings}")
                            ticket_embed.set_footer(text=f"Ticket #{counters['ticket_id'] + 1} "
                                                         f"| Use !lottery to see how Prizes work!")
                            await ctx.send(embed=ticket_embed)
                            nugs = profile[f"{ctx.author.id}"]['balance'] + calculate_prizes(player_prizes,
                                                                                             ticket_prizes)
                            profile_update(ctx.author, nugs, 'balance')
                            counters['ticket_id'] += 1
                            file_counters.truncate(0)
                            file_counters.seek(0)
                            json.dump(counters, file_counters)
                            file_counters.close()
                else:
                    item_found = True
                    await ctx.send(embed=errors.Shop.empty_inventory_error)

        elif item.lower() in 'custom role (1 month)':
            while not item_found:
                if slot <= 8:
                    slot += 1
                    item_id = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['item_id']
                    if item_id == "role_01":
                        amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['amount'] - 1
                        if amnt == 0:
                            updated_slot = {'item_id': "empty_00", "amount": 0}
                        else:
                            updated_slot = {'item_id': "role_01", "amount": amnt}
                        profile_update(ctx.author, updated_slot, 'inventory', f'slot{slot}')
                        item_found = True

                        present_embed = discord.Embed(color=ctx.author.color)
                        present_embed.add_field(name="**You have redeemed a Custom Role for 1 Month!**",
                                                value=f"I have removed 1 `Custom Role (1 Month)` from your inventory, but"
                                                      f" at the current moment I can't add roles to you! Please DM a CM "
                                                      f"or Pav and they will get you sorted!"
                                                      f"\n\nFor security, tell them this code: "
                                                      f"**ESC{random.randint(9999, 99999)}**")
                        await ctx.send(embed=present_embed)
                else:
                    item_found = True
                    await ctx.send(embed=errors.Shop.empty_inventory_error)

        elif item.lower() in 'christmas present':
            while not item_found:
                if slot <= 8:
                    slot += 1
                    item_id = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['item_id']
                    if item_id == "present_03":
                        amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}']['amount'] - 1
                        if amnt == 0:
                            updated_slot = {'item_id': "empty_00", "amount": 0}
                        else:
                            updated_slot = {'item_id': "present_03", "amount": amnt}
                        profile_update(ctx.author, updated_slot, 'inventory', f'slot{slot}')
                        item_found = True

                        choice = random.choices(present_choices, weights=(1, 3, 5, 3, 2, 1, 0.5), k=1)[0]
                        choice = choice.split(';')
                        if choice[0] == 'nugs':
                            await bank.Bank.edit(self, ctx, ctx.author, int(choice[1]), True)
                            answer = f"{choice[1]} Nugs!\nThey have been added to your balance!"
                        elif choice[0] == 'coal':
                            answer = 'Coal :(\nLooks like someone has been a naughty child!'
                        else:
                            await Inventory.add(self, ctx, ctx.author, choice[0], int(choice[1]), True)
                            answer = f'{choice[1]} {config["inv_items"][choice[0]]}(s)!\nThe item(s) have been added ' \
                                     f'to your inventory!'

                        present_embed = discord.Embed(color=ctx.author.color)
                        present_embed.add_field(name="**You open your present and you get...**",
                                                value=f"{answer}\n\nMerry Christmas!!!")
                        await ctx.send(embed=present_embed)
                else:
                    item_found = True
                    await ctx.send(embed=errors.Shop.empty_inventory_error)

    @commands.command(help="See a list of how lottery tickets work!")
    async def lottery(self, ctx):
        help_embed = discord.Embed(color=ctx.author.color)
        help_embed.add_field(name="**How Prizes Work**",
                             value="There are 4 types of prizes:\n\n"
                                   "**Normal**\n"
                                   ":gem: - 2 nugs, :ringed_planet: - 3 nugs, "
                                   ":tangerine: - 4 nugs, <:grassyE:840170557508026368> - 7 nugs,"
                                   " <:goldenE:857714717153689610> - 15 nugs\n\n"
                                   "**Jackpot**\n"
                                   "When you get 5 of the same scratchable, you get 2x the prize!\n\n"
                                   "**Ultimate Jackpot**\n"
                                   "When you get 1 of each scratchable, you get 5x the prize!\n\n"
                                   "**NEW! Exquisite**\n"
                                   "If you get the :heart_on_fire: scratchable, you get an additional 30 nugs!\n\n"
                                   "Nugs are added automatically!", inline=False)
        await ctx.send(embed=help_embed)
