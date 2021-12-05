import discord
from discord.ext import commands
import json
from functions import profile_update, calculate_prizes
import functions as func
import errors
import random
from datetime import datetime, timedelta

config = json.load(open("./../thorny_data/config.json", "r"))


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['inv'], invoke_without_command=True, help="See your or a person's Inventory")
    async def inventory(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        func.profile_update(user)
        kingdom = func.get_user_kingdom(ctx, user)

        profile_json = json.load(open('./../thorny_data/profiles.json', 'r'))
        kingdom_json = json.load(open('./../thorny_data/kingdoms.json', 'r+'))
        inventory_list = ''
        for slot in range(1, 10):
            inv_slot = profile_json[f"{user.id}"]["inventory"][f"slot{slot}"]
            inventory_list = f'{inventory_list}<:ar_ye:862635275837243402> ' \
                             f'{inv_slot["amount"]} **|** {config["inv_items"][inv_slot["item_id"]]}\n'
        inventory_embed = discord.Embed(colour=0xF5DF4D)
        inventory_embed.set_author(name=user, icon_url=user.avatar_url)
        if kingdom == "None":
            inventory_embed.add_field(name="**Financials**",
                                      value=f"**Personal Balance:** "
                                            f"<:Nug:884320353202081833>{profile_json[f'{user.id}']['balance']}\n")
        else:
            inventory_embed.add_field(name="**Financials**",
                                      value=f"**Personal Balance:** "
                                            f"<:Nug:884320353202081833>{profile_json[f'{user.id}']['balance']}\n"
                                            f"**{kingdom.capitalize()} Treasury:** "
                                            f"<:Nug:884320353202081833>{kingdom_json[kingdom]}")
        inventory_embed.add_field(name=f"**Inventory**", value=inventory_list, inline=False)
        inventory_embed.set_footer(text="Use !redeem <item> to redeem Roles & Tickets!")
        await ctx.send(embed=inventory_embed)

    @inventory.command(hidden=True, help="Add items to a player's inventory. Items: role_01, ticket_02, present_03")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.User = None, item=None, amnt=1):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_found = False
        slot = 0

        if item in config["inv_items"]:
            while not item_found:
                if slot <= 8:
                    slot += 1
                    item_id = profile[f"{user.id}"]['inventory'][f'slot{slot}']['item_id']
                    if item_id == item:
                        amnt += profile[f"{user.id}"]['inventory'][f'slot{slot}']['amount']
                        updated_slot = {'item_id': item, "amount": amnt}
                        profile_update(user, updated_slot, 'inventory', f'slot{slot}')
                        item_found = True
                        await ctx.send(f"Added {item} to {user}'s Inventory!")
                else:
                    for i in range(1, 10):
                        item_id = profile[f"{user.id}"]['inventory'][f'slot{i}']['item_id']
                        if item_id == "empty_00" and not item_found:
                            amnt += profile[f"{user.id}"]['inventory'][f'slot{i}']['amount']
                            updated_slot = {'item_id': item, "amount": amnt}
                            profile_update(user, updated_slot, 'inventory', f'slot{i}')
                            item_found = True
                            await ctx.send(f"Added {item} to {user}'s Inventory!")

    @inventory.command(hidden=True, help="Remove items from player's inventory. "
                                         "Items: role_01, ticket_02, present_03")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.User = None, item=None, amnt=None):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_found = False
        slot = 0

        if item in config["inv_items"]:
            while not item_found:
                slot += 1
                item_id = profile[f"{user.id}"]['inventory'][f'slot{slot}']['item_id']

                if item_id == item:
                    if amnt is None:
                        updated_slot = {'item_id': "empty_00", "amount": 0}
                    else:
                        amnt = profile[f"{user.id}"]['inventory'][f'slot{slot}']['amount'] - int(amnt)
                        if amnt <= 0:
                            updated_slot = {'item_id': "empty_00", "amount": 0}
                        else:
                            updated_slot = {'item_id': item, "amount": amnt}
                    profile_update(user, updated_slot, 'inventory', f'slot{slot}')
                    item_found = True
                    await ctx.send(f"Removed {item} to {user}'s Inventory!")
                else:
                    pass

    @commands.group(invoke_without_command=True, help="Get a list of all items available in the store")
    async def store(self, ctx):
        await ctx.send('Items in the Store:\n'
                       'Ticket - 14 nugs\n'
                       'Use `!store buy <item>` to buy an item!')

    @store.command(help="Purchase an item from the store. Items: Ticket")
    async def buy(self, ctx, item):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_found = False
        slot = 0

        if item.lower() in 'scratch ticket':
            if profile[f'{ctx.author.id}']['balance'] - 14 >= 0:
                new_balance = profile[f"{ctx.author.id}"]['balance'] - 14
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
                    await bank_log.send(embed=func.log_transaction(14,
                                                                   ctx.author.id,
                                                                   "STORE",
                                                                   ['Scratch', 'Ticket']))
            else:
                await ctx.send(embed=errors.Pay.lack_nugs_error)
        else:
            await ctx.send(embed=errors.Shop.item_error)

    @commands.command(help="Redeem an item from your inventory. Items: Ticket, Role")
    async def redeem(self, ctx, item):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_found = False
        slot = 0
        ticket_prizes = [[":gem:", 1], [":ringed_planet:", 3], [":tangerine:", 4], ["<:grassyE:840170557508026368>", 7],
                         ["<:goldenE:857714717153689610>", 15], [":heart_on_fire:", 30]]

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
                            file_ticket_number = open('./../thorny_data/ticket_number.json', 'r+')
                            ticket_number = json.load(file_ticket_number)
                            ticket_embed = discord.Embed(color=ctx.author.color)
                            ticket_embed.add_field(name="**Scratch Ticket**",
                                                   value=f"Scratch your ticket and see your prize!\n{player_winnings}")
                            ticket_embed.set_footer(text=f"Ticket #{ticket_number['num'] + 1} "
                                                         f"| Use !lottery to see how Prizes work!")
                            await ctx.send(embed=ticket_embed)
                            nugs = profile[f"{ctx.author.id}"]['balance'] + calculate_prizes(player_prizes,
                                                                                             ticket_prizes)
                            profile_update(ctx.author, nugs, 'balance')
                            ticket_number['num'] += 1
                            file_ticket_number.truncate(0)
                            file_ticket_number.seek(0)
                            json.dump(ticket_number, file_ticket_number)
                            file_ticket_number.close()
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

                        role_embed = discord.Embed(color=ctx.author.color)
                        role_embed.add_field(name="**You have redeemed a Custom Role for 1 Month!**",
                                             value=f"I have removed 1 `Custom Role (1 Month)` from your inventory, but"
                                                   f" at the current moment I can't add roles to you! Please DM a CM "
                                                   f"or Pav and they will get you sorted!"
                                                   f"\n\nFor security, tell them this code: "
                                                   f"**ESC{random.randint(9999, 99999)}**")
                        await ctx.send(embed=role_embed)
                else:
                    item_found = True
                    await ctx.send(embed=errors.Shop.empty_inventory_error)

    @commands.command(help="See a list of how lottery tickets work!")
    async def lottery(self, ctx):
        help_embed = discord.Embed(color=ctx.author.color)
        help_embed.add_field(name="**How Prizes Work**",
                             value="There are 4 types of prizes:\n\n"
                                   "**Normal**\n"
                                   ":gem: - 1 nug, :ringed_planet: - 3 nugs, "
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
