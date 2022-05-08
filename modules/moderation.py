import discord
from discord.ext import commands
from discord import utils

import json
from thorny_core import logs
from thorny_core.dbfactory import ThornyFactory
from thorny_core.dbcommit import commit
from thorny_core import dbevent as ev
from thorny_core import errors
from thorny_core import dbutils

config = json.load(open("./../thorny_data/config.json", "r"))


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description='CM Only | Strike someone for bad behaviour')
    @commands.has_permissions(administrator=True)
    async def strike(self, ctx, user: discord.Member, reason):
        thorny_user = await ThornyFactory.build(user)
        await thorny_user.strikes.append(ctx.author.id, reason)
        strike_embed = discord.Embed(color=0xCD853F)
        strike_embed.add_field(name=f"**{user} Got Striked!**",
                               value=f"From: {ctx.author.mention}\n"
                                     f"Reason: {reason}")
        strike_embed.set_footer(text=f"Strike ID: {thorny_user.strikes.strike_list[-1]['id']}")
        await ctx.respond(embed=strike_embed)
        await commit(thorny_user)

    @commands.slash_command(description='CM Only | Send someone to the Gulag')
    @commands.has_permissions(administrator=True)
    async def gulag(self, ctx, user: discord.Member):
        timeout_role = discord.utils.get(ctx.guild.roles, name="Time Out")
        citizen_role = discord.utils.get(ctx.guild.roles, name="Citizen")
        not_playing_role = discord.utils.get(ctx.guild.roles, name="Not Playing")
        if timeout_role not in user.roles:
            if citizen_role in user.roles:
                await user.remove_roles(citizen_role)
            elif not_playing_role in user.roles:
                await user.remove_roles(not_playing_role)
            await user.add_roles(timeout_role)
            await ctx.respond(f"{user.display_name} Has entered the Gulag! "
                              f"https://tenor.com/view/ba-sing-se-gif-20976912")
        else:
            await user.remove_roles(timeout_role)
            await user.add_roles(citizen_role)
            await ctx.respond(f"{user.display_name} Has left the Gulag! "
                              f"https://tenor.com/view/ba-sing-se-gif-20976912")

    mod = discord.SlashCommandGroup("mod", "Mod-Only commands")

    @mod.command(description="Edit someone's balance")
    @commands.has_permissions(administrator=True)
    async def baledit(self, ctx, user: discord.Member,
                      amount: discord.Option(int, "Put a - if you want to remove nugs")):
        # bank_log = self.client.get_channel(config['channels']['bank_logs'])
        # await bank_log.send(embed=logs.balance_edit(ctx.author.id, user.id, amount))

        thorny_user = await ThornyFactory.build(user)
        thorny_user.balance += amount

        if 'edit' in ctx.command.qualified_name.lower():
            await ctx.respond(f"{user}'s balance is now **{thorny_user.balance}**! (Added/Removed: {amount})")
        await commit(thorny_user)

    @staticmethod
    async def get_items(ctx):
        selector = dbutils.Base()
        item_types = await selector.select("*", "item_type")
        item_list = []
        for item in item_types:
            item_list.append(item['friendly_id'])
        return item_list

    @mod.command(description="CM Only | Add an item to a user's inventory")
    @commands.has_permissions(administrator=True)
    async def invadd(self, ctx, user: discord.Member,
                     item_id: discord.Option(str, "Select an item to add",
                                             autocomplete=utils.basic_autocomplete(get_items)), count: int = 1):
        thorny_user = await ThornyFactory.build(user)

        item_added = False
        count_error = False
        display_name = None
        item = thorny_user.inventory.fetch(item_id)
        if item is None:
            count_error, item_added = thorny_user.inventory.append(item_id, count)
        else:
            if item.item_count + count <= item.item_max_count:
                item.item_count += count
                item_added = True
            else:
                count_error = True

        for item in thorny_user.inventory.all_item_metadata:
            if item["friendly_id"] == item_id:
                if count_error and 'add' in ctx.command.qualified_name.lower():
                    await ctx.respond(f"Maximum count for this item is {item['max_item_count']}")
                elif count_error and 'buy' in ctx.command.qualified_name.lower():
                    await ctx.respond(f"You can't buy any more! Maximum amount is **{item['max_item_count']}**")
                else:
                    item_added = True
                    display_name = item['display_name']

        if item_added and 'add' in ctx.command.qualified_name.lower():
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Added Item Successfully**",
                                     value=f"Added {count}x `{display_name}` to {user}'s Inventory")
            await ctx.respond(embed=inv_edit_embed)
        elif item_added and 'buy' in ctx.command.qualified_name.lower():
            await commit(thorny_user)
            return item_added
        await commit(thorny_user)

    @mod.command(description="CM Only | Remove or clear an item from a user's inventory")
    @commands.has_permissions(administrator=True)
    async def invremove(self, ctx, user: discord.Member,
                        item_id: discord.Option(str, "Select an item to redeem",
                                                autocomplete=utils.basic_autocomplete(get_items)), count: int = None):
        thorny_user = await ThornyFactory.build(user)

        item_removed = False
        display_name = None
        item = thorny_user.inventory.fetch(item_id)
        if item is None:
            await ctx.respond(embed=errors.Inventory.item_missing_error, ephemeral=True)
        else:
            if count is None or item.item_count - count <= 0:
                thorny_user.inventory.slots.remove(item)
                count = item.item_count
                item_removed = True
            elif item.item_count - count > 0:
                item.item_count -= count
                item_removed = True

        for item in thorny_user.inventory.all_item_metadata:
            if item["friendly_id"] == item_id:
                display_name = item['display_name']

        if item_removed and 'remove' in ctx.command.qualified_name.lower():
            inv_edit_embed = discord.Embed(colour=ctx.author.colour)
            inv_edit_embed.add_field(name="**Inventory Removed Successfully**",
                                     value=f"Removed {count}x `{display_name}` "
                                           f"from {user}'s Inventory")
            await ctx.respond(embed=inv_edit_embed)
        elif item_removed and 'redeem' in ctx.command.qualified_name.lower():
            await commit(thorny_user)
            return item_removed
        await commit(thorny_user)

    @mod.command(description="CM Only | Edit prices of items (0 to remove from the store)")
    @commands.has_permissions(administrator=True)
    async def setprice(self, ctx, item_id: discord.Option(str, "Select an item to redeem",
                                                          autocomplete=utils.basic_autocomplete(get_items)),
                       price: int):
        selector = dbutils.Base()
        updated = await selector.update("item_cost", price, "item_type", "friendly_id", item_id)
        if updated:
            await ctx.respond(f"Done! {item_id} is now {price} Nugs", ephemeral=True)

    @mod.command(description="Force connect a user")
    @commands.has_permissions(administrator=True)
    async def connect(self, ctx, user: discord.Member):
        thorny_user = await ThornyFactory.build(user)

        connection: ev.ConnectEvent = await ev.fetch(ev.ConnectEvent, thorny_user, self.client)
        metadata = await connection.log_event_in_database()

        if metadata.database_log:
            await connection.log_event_in_discord()

            response_embed = discord.Embed(title="Playing? On Everthorn?! :smile:",
                                           color=0x00FF7F)
            response_embed.add_field(name=f"**One, Two, Thirty!**",
                                     value=f"I'm adding up your seconds, so when you stop playing, use `/disconnect`")
            response_embed.add_field(name=f"**View Your Playtime:**",
                                     value="`/profile view` - See your profile\n`/online` - See who else is on!",
                                     inline=False)
            response_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            response_embed.set_footer(text=f'{metadata.event_time}')
            await ctx.respond(f"{user.mention}, you have been connected by {ctx.author}", embed=response_embed)
        else:
            await ctx.respond(embed=errors.Activity.already_connected_error, ephemeral=True)

    @mod.command(description="Force disconnect a user")
    @commands.has_permissions(administrator=True)
    async def disconnect(self, ctx, user: discord.Member):
        thorny_user = await ThornyFactory.build(user)

        connection: ev.DisconnectEvent = await ev.fetch(ev.DisconnectEvent, thorny_user, self.client)
        connection.metadata.event_comment = f"Force disconnect by {ctx.author}"
        metadata = await connection.log_event_in_database()

        if metadata.database_log:
            playtime = str(metadata.playtime).split(":")
            await connection.log_event_in_discord()

            response_embed = discord.Embed(title="Nooo Don't Go So Soon! :cry:", color=0xFF5F15)
            if metadata.playtime_overtime:
                stats = f'You were connected for over 12 hours, so I brought your playtime down.' \
                        f'I set it to **1h05m**.'
            else:
                stats = f'You played for a total of **{playtime[0]}h{playtime[1]}m** this session. Nice!'
            response_embed.add_field(name=f"**Here's your stats:**",
                                     value=f'{stats}')
            response_embed.add_field(name=f"**Adjust Your Hours:**",
                                     value="Did you forget to disconnect for many hours? Use the `/adjust` command "
                                           "to bring your hours down!\n**Example:** `/adjust 2h34m` | Brings "
                                           "it down by 2 hours and 34 minutes", inline=False)
            response_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            response_embed.set_footer(text=f'{metadata.event_time}')
            await ctx.respond(f"{user.mention}, you have been disconnected by {ctx.author}", embed=response_embed)
        else:
            await ctx.respond(embed=errors.Activity.connect_error, ephemeral=True)

    @mod.command(description="Adjust a user's playtime")
    @commands.has_permissions(administrator=True)
    async def adjust(self, ctx, user: discord.Member,
                     hours: discord.Option(int, "Put a - if you want to add hours") = None,
                     minutes: discord.Option(int, "Put a - if you want to add minutes") = None):
        thorny_user = await ThornyFactory.build(user)
        event: ev.AdjustEvent = await ev.fetch(ev.AdjustEvent, thorny_user, self.client)
        event.metadata.adjusting_hour = hours
        event.metadata.adjusting_minute = minutes
        metadata = await event.log_event_in_database()

        if metadata.database_log:
            await ctx.respond(f'{user.mention}, your most recent playtime has been reduced by '
                              f'{hours or 0}h{minutes or 0}m.')
        else:
            await ctx.respond("You are already connected", ephemeral=True)

    @mod.command(description="Force level up a user")
    @commands.has_permissions(administrator=True)
    async def levelup(self, ctx, user: discord.Member, level: int):
        thorny_user = await ThornyFactory.build(user)
        required_xp = 100
        for lvl in range(1, level):
            required_xp += (lvl ** 2) * 4 + (50 * lvl) + 100

        thorny_user.profile.required_xp = required_xp
        thorny_user.profile.level = level - 1
        thorny_user.profile.xp = required_xp - 1
        await ctx.respond(f"{thorny_user.username} is now at Level {thorny_user.profile.level}.\n"
                          f"They are 1xp away from Level {level}.")
        await commit(thorny_user)
