import asyncio
import discord
from discord.ext import commands

import json
from thorny_core import errors
from thorny_core import dbutils
from thorny_core.db import UserFactory, commit
from discord import utils
from thorny_core import dbevent as ev
from thorny_core.modules import redeemingfuncs

config = json.load(open("./../thorny_data/config.json", "r"))
vers = json.load(open('version.json', 'r'))
v = vers["version"]


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def get_items(ctx):
        selector = dbutils.Base()
        item_data_list = await selector.select("*", "item_type")
        item_list = []
        for item_data in item_data_list:
            item_list.append(item_data["friendly_id"])
        return item_list

    inventory = discord.SlashCommandGroup("inventory", "Inventory Commands")

    @inventory.command(description="See you or a person's Inventory")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        thorny_user = await UserFactory.build(user)

        personal_bal = f"**Personal Balance:** <:Nug:884320353202081833>{thorny_user.balance}"
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
        inventory_embed.add_field(name=f'**Financials:**', value=f"{personal_bal}")
        inventory_embed.add_field(name=f"**Inventory**", value=inventory_text, inline=False)
        inventory_embed.set_footer(text="Redeem your items using /redeem")
        await ctx.respond(embed=inventory_embed)

    @inventory.command(description="CM Only | Add an item to a user's inventory")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.Member,
                  item_id: discord.Option(str, "Select an item to add",
                                          autocomplete=utils.basic_autocomplete(get_items)), count: int = 1):
        thorny_user = await UserFactory.build(user)

        try:
            thorny_user.inventory.add_item(item_id, count)
        except errors.ItemMaxCountError:
            item = thorny_user.inventory.data(item_id)
            raise errors.ItemMaxCountError(item.item_max_count)
        else:
            item = thorny_user.inventory.fetch(item_id)
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Added Item Successfully**",
                                     value=f"Added {count}x `{item.item_display_name}` to {user}'s Inventory")
            await ctx.respond(embed=inv_edit_embed)
            await commit(thorny_user)

    @inventory.command(description="CM Only | Remove or clear an item from a user's inventory")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member,
                     item_id: discord.Option(str, "Select an item to redeem",
                                             autocomplete=utils.basic_autocomplete(get_items)), count: int = None):
        thorny_user = await UserFactory.build(user)
        item = thorny_user.inventory.fetch(item_id)

        try:
            thorny_user.inventory.remove_item(item_id, count)
        except errors.MissingItemError:
            raise errors.MissingItemError()
        else:
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Inventory Removed Successfully**",
                                     value=f"Removed {count}x `{item.item_display_name}` "
                                           f"from {user}'s Inventory")
            await ctx.respond(embed=inv_edit_embed)
            await commit(thorny_user)

    store = discord.SlashCommandGroup("store", "Store Commands")

    @store.command(description="CM Only | Edit prices of items (0 to remove from the store)")
    @commands.has_permissions(administrator=True)
    async def setprice(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                          autocomplete=utils.basic_autocomplete(get_items)),
                       price: int):
        selector = dbutils.Base()
        updated = await selector.update("item_cost", price, "item_type", "friendly_id", item_id)
        if updated:
            await ctx.respond(f"Done! {item_id} is now {price} Nugs", ephemeral=True)

    @store.command(description="Get a list of all items available in the store")
    async def catalogue(self, ctx):
        thorny_user = await UserFactory.build(ctx.author)
        item_text = ""
        for item_data in thorny_user.inventory.all_items:
            if item_data.item_cost > 0:
                item_text = f"{item_text}\n**{item_data.item_display_name}** |" \
                            f" <:Nug:884320353202081833>{item_data.item_cost}\n" \
                            f"**Item ID:** {item_data.item_id}\n"

        store_embed = discord.Embed(colour=ctx.author.colour)
        store_embed.add_field(name=f'**Items Available:**',
                              value=f"{item_text}", inline=False)
        store_embed.set_footer(text=f"{v} | Use /store buy to purchase!")
        await ctx.respond(embed=store_embed)

    @store.command(description="Purchase an item from the store")
    async def buy(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                     autocomplete=utils.basic_autocomplete(get_items)),
                  amount: int = 1):
        thorny_user = await UserFactory.build(ctx.author)
        try:
            item = thorny_user.inventory.data(item_id)
            if item.item_cost != 0:
                thorny_user.inventory.add_item(item_id, amount)
            elif item.item_cost == 0:
                raise errors.ItemNotAvailableError()

        except errors.ItemMaxCountError:
            item = thorny_user.inventory.fetch(item_id)
            raise errors.ItemMaxCountError(item.item_max_count)

        else:
            item = thorny_user.inventory.fetch(item_id)

            if item.item_cost != 0 and thorny_user.balance - item.item_cost * amount >= 0:
                thorny_user.balance -= item.item_cost * amount
                inv_edit_embed = discord.Embed(colour=ctx.author.colour)
                inv_edit_embed.add_field(name="**Cha-Ching!**",
                                         value=f"Bought {amount}x `{item.item_display_name}`")
                inv_edit_embed.set_footer(text=f"{v} | Use /redeem to redeem this item!")
                await ctx.respond(embed=inv_edit_embed)
                event: ev.Event = await ev.fetch(ev.StoreTransaction, thorny_user, self.client)
                event.edit_metadata("nugs_amount", item.item_cost * amount)
                event.edit_metadata("sender_user", ctx.author)
                event.edit_metadata("event_comment", f"Purchase of {amount}x {item.item_display_name}")
                await event.log_event_in_discord()
                await commit(thorny_user)
            elif thorny_user.balance - item.item_cost * amount < 0:
                raise errors.BrokeError()

    @commands.slash_command(description="Redeem an item from your inventory")
    async def redeem(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                        autocomplete=utils.basic_autocomplete(get_items))):

        thorny_user = await UserFactory.build(ctx.author)
        item = thorny_user.inventory.fetch(item_id)

        if item is not None and item.redeemable:
            try:
                thorny_user.inventory.remove_item(item_id, 1)

            except errors.MissingItemError:
                raise errors.MissingItemError()

            else:
                if item.item_id == 'role':
                    await redeemingfuncs.redeem_role(ctx, thorny_user, self.client)
                    await commit(thorny_user)

                elif item.item_id == 'ticket':
                    await redeemingfuncs.redeem_ticket(ctx, thorny_user)
                    await commit(thorny_user)

                elif item.item_id == "gift":
                    pass

        elif item.item_id is None:
            raise errors.MissingItemError()
        else:
            raise errors.ItemNotAvailableError()

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
