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
from thorny_core.uikit import slashoptions

config = json.load(open("./../thorny_data/config.json", "r"))
vers = json.load(open('version.json', 'r'))
v = vers["version"]


class Inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    inventory = discord.SlashCommandGroup("inventory", "Inventory Commands",
                                          guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))

    @inventory.command(description="See you or a person's Inventory")
    async def view(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(user.guild)

        if user == ctx.author:
            view_to_be_sent = views.RedeemMenu(thorny_user, thorny_guild, ctx)
        else:
            view_to_be_sent = None

        await ctx.respond(embed=embeds.inventory_embed(thorny_user, thorny_guild),
                          view=view_to_be_sent)

    @inventory.command(description="Mod Only | Add an item to a user's inventory")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.Member,
                  item_id: discord.Option(str, "Select an item to add",
                                          choices=slashoptions.slash_command_all_items()),
                  count: int = 1):
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

    @inventory.command(description="Mod Only | Remove or clear an item from a user's inventory")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user: discord.Member,
                     item_id: discord.Option(str, "Select an item to redeem",
                                             choices=slashoptions.slash_command_all_items()),
                     count: int = None):
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

        await ctx.respond(embed=embeds.store_items(thorny_user, thorny_guild),
                          view=views.Store(thorny_user, thorny_guild, ctx))

    @commands.slash_command(description="See how tickets work!",
                            guild_ids=None)
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
