import asyncio
import discord
from discord.ext import commands

import json
from thorny_core import errors
from thorny_core import dbutils
from thorny_core.db import UserFactory, commit, GuildFactory
from discord import utils
from thorny_core.uikit import embeds, views
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
        return utils.basic_autocomplete(item_list)

    inventory = discord.SlashCommandGroup("inventory", "Inventory Commands")

    @inventory.command(description="See you or a person's Inventory")
    async def view(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(user.guild)

        personal_bal = f"**Personal Balance:** {thorny_guild.currency.emoji}{thorny_user.balance}"
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
                                          autocomplete=get_items), count: int = 1):
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
                                             autocomplete=get_items), count: int = None):
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

    @commands.slash_command(description="Mod Only | Edit prices of items (0 to remove from the store)",
                            guild_ids=GuildFactory.get_guilds_by_feature('everthorn_only'))
    @commands.has_permissions(administrator=True)
    async def setprice(self, ctx, item_id: discord.Option(str, "Select an item to redeem", autocomplete=get_items),
                       price: int):
        selector = dbutils.Base()
        updated = await selector.update("item_cost", price, "item_type", "friendly_id", item_id)
        if updated:
            await ctx.respond(f"Done! {item_id} is now {price}", ephemeral=True)

    @commands.slash_command(description="Purchase items from the shop!",
                            guild_ids=GuildFactory.get_guilds_by_feature('beta'))
    async def shop(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.guild)

        await ctx.respond(embed=embeds.store_items(thorny_user, thorny_guild),
                          view=views.Store(thorny_user, thorny_guild))

    store = discord.SlashCommandGroup("store", "Store Commands")

    @store.command(description="Get a list of all items available in the store")
    async def catalogue(self, ctx):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.author.guild)

        item_text = ""
        for item_data in thorny_user.inventory.all_items:
            if item_data.item_cost > 0:
                item_text = f"{item_text}\n**{item_data.item_display_name}** |" \
                            f" {thorny_guild.currency.emoji}{item_data.item_cost}\n" \
                            f"**Item ID:** {item_data.item_id}\n"

        store_embed = discord.Embed(colour=ctx.author.colour)
        store_embed.add_field(name=f'**Items Available:**',
                              value=f"{item_text}", inline=False)
        store_embed.set_footer(text=f"{v} | Use /store buy to purchase!")
        await ctx.respond(embed=store_embed)

    @store.command(description="Purchase an item from the store")
    async def buy(self, ctx, item_id: discord.Option(str, "Select an item to redeem", autocomplete=get_items),
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
                # Add code for transactions
                await commit(thorny_user)
            elif thorny_user.balance - item.item_cost * amount < 0:
                raise errors.BrokeError()

    @commands.slash_command(description="Redeem an item from your inventory")
    async def redeem(self, ctx, item_id: discord.Option(str, "Select an item to redeem", autocomplete=get_items)):
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
        thorny_guild = await GuildFactory.build(ctx.author.guild)

        help_embed = discord.Embed(color=ctx.author.color)
        help_embed.add_field(name="**How Prizes Work**",
                             value="There are 2 types of prizes:\n\n"
                                   "**Normal Prize**\n"
                                   f":yellow_heart: - {thorny_guild.currency.emoji}1, "
                                   f":gem: - {thorny_guild.currency.emoji}2, "
                                   f":dagger: - {thorny_guild.currency.emoji}4, "
                                   f"<:grassyE:840170557508026368> - {thorny_guild.currency.emoji}6, "
                                   f"<:goldenE:857714717153689610> - {thorny_guild.currency.emoji}7, "
                                   f":dragon_face: - {thorny_guild.currency.emoji}64\n\n"
                                   "**Jackpot Prize**\n"
                                   "When you get 4 different scratchables, you get double the prize! Except for when "
                                   "you get a :dragon_face:.\n\n"
                                   f"**{thorny_guild.currency.name}** are added automatically to your balance!",
                             inline=False)
        await ctx.respond(embed=help_embed, ephemeral=True)
