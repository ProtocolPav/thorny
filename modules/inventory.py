import discord
from discord.ext import commands
import json
from functions import profile_update
import errors
from lottery import create_ticket, winners

config = json.load(open("./../thorny_data/config.json", "r"))


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['inv'], invoke_without_command=True, help="See your or a person's Inventory")
    async def inventory(self, ctx, user: discord.Member = None):
        inventory_list = ''
        profile_json = json.load(open('./../thorny_data/profiles.json', 'r'))
        kingdom_json = json.load(open('./../thorny_data/kingdoms.json', 'r+'))
        if user is None:
            person = ctx.author
        else:
            person = user
        for slot in range(1, 10):
            inv_slot = profile_json[f"{person.id}"]["inventory"][f"slot{slot}"]
            inventory_list = f'{inventory_list}<:ar_ye:862635275837243402> ' \
                             f'{inv_slot["amount"]} **|** {config["inv_items"][inv_slot["item_id"]]}\n'
        inventory_embed = discord.Embed(colour=0xF5DF4D)
        inventory_embed.set_author(name=person, icon_url=person.avatar_url)
        inventory_embed.add_field(name="**Financials**",
                                  value=f"**Personal Balance:** "
                                        f"<:Nug:884320353202081833>{profile_json[f'{person.id}']['balance']}\n"
                                        f"**{profile_json[f'{person.id}']['kingdom'].capitalize()} Treasury:** "
                                        f"<:Nug:884320353202081833>{kingdom_json[profile_json[f'{person.id}']['kingdom']]}")
        inventory_embed.add_field(name=f"**Inventory**", value=inventory_list, inline=False)
        inventory_embed.set_footer(text="BETA | Use !redeem <item> to redeem Roles & Tickets!")
        await ctx.send(embed=inventory_embed)

    @inventory.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.User = None, item=None, amnt=1):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_placed = False
        slot = 0

        if item.lower() == 'role' or item.lower() == 'custom':
            while not item_placed:
                slot += 1
                if profile[f"{user.id}"]['inventory'][f'slot{slot}'] == 'Empty' or \
                        profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Custom Role 1m":
                    profile_update(user, 'Custom Role 1m', 'inventory', f'slot{slot}')
                    amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}_amount'] + int(amnt)
                    profile_update(user, amnt, 'inventory', f'slot{slot}_amount')
                    item_placed = True
                    await ctx.send(f'Added item {item} to slot {slot}')
                else:
                    pass
        elif item.lower() == 'ticket' or item.lower() == 'lottery':
            while not item_placed:
                slot += 1
                if profile[f"{user.id}"]['inventory'][f'slot{slot}'] == 'Empty' or \
                        profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Ticket":
                    profile_update(user, 'Ticket', 'inventory', f'slot{slot}')
                    amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}_amount'] + int(amnt)
                    profile_update(user, amnt, 'inventory', f'slot{slot}_amount')
                    item_placed = True
                    await ctx.send(f'Added item {item} to slot {slot}')
                else:
                    pass

    @inventory.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.User = None, item=None):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_removed = False
        slot = 0

        if item.lower() == 'role' or item.lower() == 'custom':
            while not item_removed:
                slot += 1
                if profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Custom Role 1m":
                    profile_update(user, 'Empty', 'inventory', f'slot{slot}')
                    profile_update(user, 0, 'inventory', f'slot{slot}_amount')
                    item_removed = True
                    await ctx.send(f'Removed item {item} from slot {slot}')
                else:
                    pass
        elif item.lower() == 'ticket' or item.lower() == 'lottery':
            while not item_removed:
                slot += 1
                if profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Ticket":
                    profile_update(user, 'Empty', 'inventory', f'slot{slot}')
                    profile_update(user, 0, 'inventory', f'slot{slot}_amount')
                    item_removed = True
                    await ctx.send(f'Removed item {item} from slot {slot}')
                else:
                    pass

    @commands.group(invoke_without_command=True)
    async def store(self, ctx):
        await ctx.send('Items in the Store:\n'
                       'Lottery Ticket - 10n\n'
                       'Use !store buy item to buy an item!')

    @store.command()
    async def buy(self, ctx, item):
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_placed = False
        slot = 0

        if item.lower() == 'ticket' or item.lower() == 'lottery':
            if 18 <= int(datetime.now().strftime("%d")) <= 25:
                newbal = profile[f"{ctx.author.id}"]['balance'] - 10
                profile_update(ctx.author, newbal, 'balance')
                while not item_placed:
                    slot += 1
                    if profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == 'Empty' or \
                            profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == 'Ticket':
                        amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}_amount'] + 1
                        profile_update(ctx.author, 'Ticket', 'inventory', f'slot{slot}')
                        profile_update(ctx.author, amnt, 'inventory', f'slot{slot}_amount')
                        item_placed = True
                        ticket_number = create_ticket(ctx.author, 1)
                        await ctx.send('Bought a ticket!')
                        await ctx.author.send(f"Your ticket is {ticket_number}")
                    else:
                        pass
            else:
                await ctx.send(embed=errors.Shop.ticket_buy_error)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def getwinners(self, ctx):
        winners_list = winners(thorny)
        await ctx.send(winners_list)