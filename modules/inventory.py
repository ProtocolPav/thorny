import asyncio
import discord
from discord.ext import commands

import json
from thorny_core import errors
from thorny_core.db import UserFactory, commit, GuildFactory
import thorny_core.uikit as uikit

config = json.load(open("./../thorny_data/config.json", "r"))
vers = json.load(open('version.json', 'r'))
v = vers["version"]


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    inventory = discord.SlashCommandGroup("inventory", "Inventory Commands")

    @inventory.command(description="See you or a person's Inventory",
                       guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    async def view(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(user.guild)

        if user == ctx.author:
            view_to_be_sent = uikit.RedeemMenu(thorny_user, thorny_guild, ctx)
        else:
            view_to_be_sent = None

        await ctx.respond(embed=uikit.inventory_embed(thorny_user, thorny_guild),
                          view=view_to_be_sent)

    @inventory.command(description="Mod Only | Add an item to a user's inventory",
                       guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.Member,
                  item_id: discord.Option(str, "Select an item to add",
                                          choices=uikit.slash_command_all_items()),
                  count: int = 1):
        thorny_user = await UserFactory.build(user)
        item = thorny_user.inventory.get_item(item_id)

        try:
            thorny_user.inventory.add_item(item_id, count)

            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Added Item Successfully**",
                                     value=f"Added {count}x `{item.item_display_name}` to {user}'s Inventory")

            await ctx.respond(embed=inv_edit_embed)
            await commit(thorny_user)
        except errors.ItemMaxCountError:
            raise errors.ItemMaxCountError(item.item_max_count)

    @inventory.command(description="Mod Only | Remove or clear an item from a user's inventory",
                       guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member,
                     item_id: discord.Option(str, "Select an item to redeem",
                                             choices=uikit.slash_command_all_items()),
                     count: int = None):
        thorny_user = await UserFactory.build(user)
        item = thorny_user.inventory.get_item(item_id)

        if count is None:
            count = item.item_count

        try:
            thorny_user.inventory.remove_item(item_id, count)

            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Inventory Removed Successfully**",
                                     value=f"Removed {count}x `{item.item_display_name}` from {user}'s Inventory")

            await ctx.respond(embed=inv_edit_embed)
            await commit(thorny_user)
        except errors.MissingItemError:
            raise errors.MissingItemError()

    # @commands.slash_command(description="Mod Only | Edit prices of items (0 to remove from the store)",
    #                         guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    # @commands.has_permissions(administrator=True)
    # async def setprice(self, ctx,
    #                    item_id: discord.Option(str, "Select an item to redeem", choices=slashoptions.slash_command_all_items()),
    #                    price: int):
    #     selector = dbutils.Base()
    #     updated = await selector.update("item_cost", price, "item_type", "friendly_id", item_id)
    #     if updated:
    #         await ctx.respond(f"Done! {item_id} is now {price}", ephemeral=True)

    @commands.slash_command(description="Purchase items from the shop!",
                            guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    async def shop(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.guild)

        await ctx.respond(embed=uikit.store_items(thorny_user, thorny_guild),
                          view=uikit.Store(thorny_user, thorny_guild, ctx))
