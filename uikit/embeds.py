import discord
import json

from datetime import datetime
from dateutil.relativedelta import relativedelta
from thorny_core.db import user, guild, GuildFactory, generator
import giphy_client
import random

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]
config = json.load(open('../thorny_data/config.json', 'r+'))
api_instance = giphy_client.DefaultApi()
giphy_token = config["giphy_token"]


def ping_embed(client: discord.Bot, bot_started_on: datetime):
    uptime = datetime.now().replace(microsecond=0) - bot_started_on

    embed = discord.Embed(color=0x228B22)
    embed.add_field(name="Hey! I'm Thorny!",
                    value=f"*Always here to help!*\n\n"
                          f"**Current Version:** {v}\n"
                          f"**Ping:** {round(client.latency * 1000)}ms\n"
                          f"**Uptime:** {uptime}\n"
                          f"Operating on {len(client.guilds)} Guilds\n"
                          f"Processing {round(len(client.application_commands))}+ slash commands")
    embed.set_thumbnail(url=client.user.avatar.url)

    return embed


async def profile_main_embed(thorny_user: user.User, is_donator) -> discord.Embed:
    thorny_guild = await GuildFactory.build(thorny_user.discord_member.guild)

    main_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan or thorny_user.profile.default_slogan}",
                                    color=thorny_user.discord_member.color)
    main_page_embed.set_author(name=thorny_user.discord_member, icon_url=thorny_user.discord_member.display_avatar.url)
    main_page_embed.set_thumbnail(url=thorny_user.discord_member.display_avatar.url)

    profile = thorny_user.profile
    last_month = (datetime.now() - relativedelta(months=1)).strftime('%B')
    two_months_ago = (datetime.now() - relativedelta(months=2)).strftime('%B')

    main_page_embed.add_field(name=f"**:card_index: Information**",
                              value=f"{is_donator}\n"
                                    f"**Gamertag:** {profile.gamertag or profile.default_gamertag}\n"
                                    f"**Level:** {thorny_user.level.level}\n"
                                    f"**Balance:** {thorny_guild.currency.emoji} {thorny_user.balance}\n"
                                    f"**Birthday:** {thorny_user.birthday}\n"
                                    f"**Age:** {thorny_user.age}\n"
                                    f"**Joined on:** {thorny_user.join_date}"
                              )

    main_page_embed.add_field(name=f"**:clock8: Quick Stats**",
                              value=f"**Today:** {thorny_user.playtime.todays_playtime}\n"
                                    f"**{datetime.now().strftime('%B')}:** {thorny_user.playtime.current_playtime}\n"
                                    f"**{last_month}:** {thorny_user.playtime.previous_playtime}\n"
                                    f"**{two_months_ago}:** {thorny_user.playtime.expiring_playtime}\n"
                                    f"**Total:** {thorny_user.playtime.total_playtime}\n",
                              inline=True)

    main_page_embed.add_field(name=f"**:person_raising_hand: About Me**",
                              value=f'"{profile.aboutme or profile.default_aboutme}"',
                              inline=False)

    main_page_embed.set_footer(text=f"{v} | Main Page")

    return main_page_embed


async def profile_lore_embed(thorny_user: user.User) -> discord.Embed:
    lore_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan or thorny_user.profile.default_slogan}",
                                    color=thorny_user.discord_member.color)

    lore_page_embed.set_author(name=thorny_user.discord_member,
                               icon_url=thorny_user.discord_member.display_avatar.url)
    lore_page_embed.set_thumbnail(url=thorny_user.discord_member.display_avatar.url)

    emoji = "⦿"
    profile = thorny_user.profile

    lore_page_embed.add_field(name="🦹 My Character",
                              value=f"**Name:** {profile.character_name}\n"
                                    f"**Age:** {profile.character_age}\n"
                                    f"**Race:** {profile.character_race}\n"
                                    f"**Role:** {profile.character_role}\n"
                                    f"**Origin:** {profile.character_origin}\n"
                                    f"**Beliefs:** {profile.character_beliefs}\n"
                              )

    lore_page_embed.add_field(name="🏹 Skills",
                              value=f"**Agility:** {emoji * profile.agility}\n"
                                    f"**Valor:** {emoji * profile.valor}\n"
                                    f"**Strength:** {emoji * profile.strength}\n"
                                    f"**Charisma:** {emoji * profile.charisma}\n"
                                    f"**Creativity:** {emoji * profile.creativity}\n"
                                    f"**Ingenuity:** {emoji * profile.ingenuity}\n"
                              )

    lore_page_embed.add_field(name=f"**:dart: Character Backstory**",
                              value=f'"{thorny_user.profile.lore}"',
                              inline=False)

    lore_page_embed.set_footer(text=f"{v} | Lore")

    return lore_page_embed


async def profile_stats_embed(thorny_user: user.User) -> discord.Embed:
    stats_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan or thorny_user.profile.default_slogan}",
                                     color=thorny_user.discord_member.color)

    stats_page_embed.set_author(name=thorny_user.discord_member,
                                icon_url=thorny_user.discord_member.display_avatar.url)

    last_month = (datetime.now() - relativedelta(months=1)).strftime('%B')
    two_months_ago = (datetime.now() - relativedelta(months=2)).strftime('%B')

    leaderboard, rank = await generator.activity_leaderboard(thorny_user, datetime.now())

    stats_page_embed.add_field(name=f"**:clock8: Today's Roundup**",
                               value=f"You played for **{thorny_user.playtime.todays_playtime}** today",
                               inline=True)

    stats_page_embed.add_field(name=f"**:clock8: Monthly Hours**",
                               value=f"**{datetime.now().strftime('%B')}:** {thorny_user.playtime.current_playtime}\n"
                                     f"**{last_month}:** {thorny_user.playtime.previous_playtime}\n"
                                     f"**{two_months_ago}:** {thorny_user.playtime.expiring_playtime}\n"
                                     f"**Total:** {thorny_user.playtime.total_playtime}\n",
                               inline=True)

    stats_page_embed.add_field(name=f"**:clock8: Monthly Roundup**",
                               value=f"You played for **{thorny_user.playtime.todays_playtime}** today\n"
                                     f"You are #{rank} on {datetime.now().strftime('%B')}'s Leaderboard\n",
                               inline=False)

    stats_page_embed.add_field(name=f"**🔜 More Stats Coming Soon...**",
                               value=f"I'm working *really* hard at analyzing your playtime. Soon I'll come back with"
                                     f" more cool stats, and even a graph!",
                               inline=False)

    stats_page_embed.set_footer(text=f"{v} | Playtime Stats")

    return stats_page_embed


async def profile_edit_embed(thorny_user: user.User) -> discord.Embed:
    edit_embed = discord.Embed(title="Editing Your Profile",
                               colour=thorny_user.discord_member.colour)

    edit_embed.add_field(name="It's simple, really!",
                         value=f"The Profile is separated into 3 pages:\n"
                               f"<:_pink:921708790322192396> The Main Page, all about **YOU**\n"
                               f"<:_purple:921708790368309269> The Lore Page, all about your character\n"
                               f"<:_orange:921708790099898419> The Playtime Stats Page, which gives deep insight\n"
                               f"\nAnd so, the **Editing Menus** are split up just the same!\n"
                               f"You have 3 **select Menus** to choose from, for each of the 3 **pages**!\n\n"
                               f"**Now, just choose a section from the menus below and start editing!**")

    return edit_embed


async def application_info_embed(thorny_user: user.User, modal_children: discord.ui.Modal.children):
    info_embed = discord.Embed(title=modal_children[0].value,
                               colour=0xFDDA0D)
    info_embed.set_author(name=thorny_user.username,
                          icon_url=thorny_user.discord_member.display_avatar.url)

    info_embed.add_field(name="Project Info:",
                         value=f"**Coordinates:** {modal_children[1].value}\n"
                               f"**Road Built:** {modal_children[2].value}\n"
                               f"**Project Members:** {thorny_user.discord_member.name}, {modal_children[4].value}")

    info_embed.add_field(name="Project Idea & Time Estimation:",
                         value=f"{modal_children[3].value}",
                         inline=False)

    info_embed.add_field(name="CM Comments:",
                         value="If a CM has any comments, they will be added here",
                         inline=False)

    info_embed.add_field(name="**STATUS**",
                         value="IN REVIEW...",
                         inline=False)

    info_embed.set_footer(text=f"{thorny_user.user_id}")

    return info_embed


def configure_embed(thorny_guild: guild.Guild) -> dict[str, discord.Embed]:
    welcome_embed = discord.Embed(title="Configuring Welcome Settings",
                                  colour=0xD7E99A)
    welcome_embed.add_field(name="Current Settings",
                            value=f"**Join, Leave and Birthday Messages Channel:** <#{thorny_guild.channels.welcome_channel}>\n\n"
                                  f"**Join Message:** {thorny_guild.join_message}\n"
                                  f"**Leave Message:** {thorny_guild.leave_message}\n"
                                  f"**Birthday Message:** Currently not available",
                            inline=False)
    welcome_embed.add_field(name="Note",
                            value="When editing the **channel**, enter the channel ID!\n"
                                  "Press and hold (mobile) or right click (PC) on the channel, and copy ID.",
                            inline=False)

    levels_embed = discord.Embed(title="Configuring Levels",
                                 colour=0xD7E99A)
    enabled_disabled = "ENABLED" if thorny_guild.levels_enabled else "DISABLED"
    levels_embed.add_field(name="Current Settings",
                           value=f"**Leveling is currently** {enabled_disabled}\n\n"
                                 f"**Level Up Message:** {thorny_guild.level_message}\n"
                                 f"**XP Multiplier:** x{thorny_guild.xp_multiplier}\n"
                                 f"**No XP Channels:** Currently not available")

    logs_embed = discord.Embed(title="Configuring Logs",
                               colour=0xD7E99A)
    logs_embed.add_field(name="Current Settings",
                         value=f"**Logs channel:** <#{thorny_guild.channels.logs_channel}>")
    logs_embed.add_field(name="Note",
                         value="When editing the **channel**, enter the channel ID!\n"
                               "Press and hold (mobile) or right click (PC) on the channel, and copy ID.",
                         inline=False)

    updates_embed = discord.Embed(title="Configuring Updates",
                                  colour=0xD7E99A)
    updates_embed.add_field(name="About Updates",
                            value=f"When Thorny receives new features, or updates to new features, you can choose to receive "
                                  f"changelogs and tutorials for new features in a channel. You can make it private or "
                                  f"public for people to see.")
    updates_embed.add_field(name="Current Settings",
                            value=f"**Thorny updates channel:** <#{thorny_guild.channels.thorny_updates_channel}>",
                            inline=False)
    updates_embed.add_field(name="Note",
                            value="When editing the **channel**, enter the channel ID!\n"
                                  "Press and hold (mobile) or right click (PC) on the channel, and copy ID.",
                            inline=False)

    gulag_embed = discord.Embed(title="Create the Gulag",
                                colour=0xD7E99A)
    gulag_embed.add_field(name="About The Gulag",
                          value="When you have troublemakers in your server, you should do something about them.\n"
                                "Thorny's Gulag is a perfect place to take these troublemakers to, so you can discuss and "
                                "help dissolve any arguments they may be having. \n"
                                "When a user is taken into the gulag, they cannot see any channel except for the gulag.")
    gulag_embed.add_field(name="Current Settings",
                          value=f"**Gulag Channel:** <#{thorny_guild.channels.gulag_channel}>\n"
                                f"**Gulag Role:** <@{thorny_guild.roles.timeout_role}>",
                          inline=False)
    gulag_embed.add_field(name="Important Note",
                          value="Before you press the **Create Channel & Role** button, you should know that Thorny will "
                                "modify channel permissions in **all** channels. Thorny will require the **Manage Channel** "
                                "permission in all of them. If it cannot manage permissions in some channels, there is a "
                                "chance that the Gulag Role will not work properly.",
                          inline=False)

    response_embed = discord.Embed(title="Edit Responses",
                                   description="Thorny picks one random response out of each list",
                                   colour=0xD7E99A)
    exact = ""
    for key, val in thorny_guild.responses.exact.items():
        exact = f"{exact}**{key}** = {','.join(val)}\n"
    response_embed.add_field(name="Exact Responses",
                             value=exact)
    wildcard = ""
    for key, val in thorny_guild.responses.wildcard.items():
        wildcard = f"{wildcard}**{key}** = {','.join(val)}\n"
    response_embed.add_field(name="Wildcard Responses",
                             value=wildcard,
                             inline=False)

    currency_embed = discord.Embed(title="Configure Server Currency",
                                   colour=0xD7E99A)
    currency_embed.add_field(name="Current Settings",
                             value=f"**Currency Name:** {thorny_guild.currency.name}\n"
                                   f"**Currency Emoji:** {thorny_guild.currency.emoji}")
    currency_embed.add_field(name="Setting Custom Emoji",
                             value="If you want to set a custom server emoji, it is a bit tricky. You must give it in this form: "
                                   "**<:EmojiName:ID>**. Luckily, discord provides a quick and easy way to get this.\n"
                                   "Simply put a backslash and then write your emoji. Press send and then copy it.\n",
                             inline=False)

    return {"welcome": welcome_embed,
            "levels": levels_embed,
            "logs": logs_embed,
            "updates": updates_embed,
            "gulag": gulag_embed,
            "responses": response_embed,
            "currency": currency_embed}


def level_up_embed(thorny_user: user.User, thorny_guild: guild.Guild) -> discord.Embed:
    api_response = api_instance.gifs_search_get(giphy_token, f"{thorny_user.level.level}", limit=10)
    gifs_list = list(api_response.data)
    gif = random.choice(gifs_list)

    embed = discord.Embed(colour=thorny_user.discord_member.colour)
    embed.set_author(name=thorny_user.username,
                     icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f":partying_face: Congrats!",
                    value=f"You leveled up to **Level {thorny_user.level.level}!**\n"
                          f"{thorny_guild.level_message}")
    embed.set_image(url=gif.images.original.url)

    return embed


def message_delete_embed(message: discord.Message, event_time: datetime):
    embed = discord.Embed(color=0xE97451)
    embed.add_field(name="**Message Deleted**",
                    value=f"Message sent by {message.author.mention} was deleted in <#{message.channel.id}>.\n"
                          f"**Contents:**\n{message.content}")
    embed.set_footer(text=event_time)

    return embed


def message_edit_embed(message: discord.Message, message_after: discord.Message, event_time: datetime):
    embed = discord.Embed(color=0x7393B3)
    embed.add_field(name="**Message Edited**",
                    value=f"Message sent by {message.author.mention} was edited.\n"
                          f"**Before:**\n{message.content}\n\n"
                          f"**After:**\n{message_after.content}")
    embed.set_footer(text=event_time)

    return embed


def user_join(thorny_user: user.User, thorny_guild: guild.Guild):
    def ordinaltg(n):
        return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

    searches = ["welcome", "hello", "heartfelt welcome", "join us", "greetings", "what's up"]
    api_response = api_instance.gifs_search_get(giphy_token, random.choice(searches), limit=10)
    gifs_list = list(api_response.data)
    gif = random.choice(gifs_list)

    embed = discord.Embed(colour=0x57945c)
    embed.add_field(name=f"**Welcome to {thorny_guild.guild_name}, {thorny_user.username}!**",
                    value=f"You are the **{ordinaltg(thorny_guild.discord_guild.member_count)}** member!\n\n"
                          f"{thorny_guild.join_message}")
    embed.set_thumbnail(url=thorny_user.discord_member.display_avatar.url)
    embed.set_image(url=gif.images.original.url)

    return embed


def user_leave(thorny_user: user.User, thorny_guild: guild.Guild):
    embed = discord.Embed(colour=0xc34184)
    embed.add_field(name=f"**{thorny_user.username} has left**",
                    value=f"{thorny_guild.leave_message}")

    return embed


def inventory_embed(thorny_user: user.User, thorny_guild: guild.Guild):
    embed = discord.Embed(color=0xE0115F)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f'**Financials:**',
                    value=f"**Personal Balance:** {thorny_guild.currency.emoji}{thorny_user.balance}")
    embed.add_field(name=f'**Inventory:**',
                    value=f"{thorny_user.inventory}",
                    inline=False)

    return embed


def balance_edit_embed(thorny_user: user.User, thorny_guild: guild.Guild, amount: int):
    embed = discord.Embed(color=0x7CFC00)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f"Successfully {'Added' if amount > 0 else 'Removed'} {abs(amount)} {thorny_guild.currency.name}",
                    value=f"Balance was **{thorny_guild.currency.emoji}{thorny_user.balance - amount}**\n"
                          f"Balance is now **{thorny_guild.currency.emoji}{thorny_user.balance}**")

    return embed


def payment_embed(thorny_user: user.User, receivable: user.User, thorny_guild: guild.Guild, amount: int, reason: str):
    embed = discord.Embed(color=0xF4C430)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f'{thorny_guild.currency.emoji} Payment Successful!',
                    value=f'**Amount paid:** {thorny_guild.currency.emoji}{amount}\n'
                          f'**Paid to:** {receivable.discord_member.mention}\n\n'
                          f'**Reason:** {reason}')
    embed.set_footer(text=f"Your balance: {thorny_user.balance} | {receivable.username}'s balance: {receivable.balance}")

    return embed


def payment_log(thorny_user: user.User, receivable: user.User, thorny_guild: guild.Guild, amount: int, reason: str):
    embed = discord.Embed(color=0xF4C430)
    embed.add_field(name="**Transaction**",
                    value=f"<@{thorny_user.discord_member.id}> paid <@{receivable.discord_member.id}> "
                          f"**{thorny_guild.currency.emoji}{amount}**\n"
                          f"**Reason:** {reason}")

    return embed


def store_items(thorny_user: user.User, thorny_guild: guild.Guild):
    embed = discord.Embed(colour=0xFFBF00,
                          title="Shop Catalogue",
                          description="Select an item from the menu to buy!")

    for item in thorny_user.inventory.all_items:
        if item.item_cost != 0:
            embed.add_field(name=f"**{item.item_display_name}** | {thorny_guild.currency.emoji}{item.item_cost}\n",
                            value=f"```{item.description} You can hold a maximum of "
                                  f"{item.item_max_count} {item.item_display_name}s```",
                            inline=False)

    return embed


def store_selected_item(thorny_user: user.User, thorny_guild: guild.Guild, item_id: str):
    embed = discord.Embed(colour=0xFFBF00,
                          title="Shop Catalogue")

    item = thorny_user.inventory.fetch(item_id)

    embed.add_field(name=f"**About {item.item_display_name}**",
                    value=f"```{item.description}```\n"
                          f"**Cost:** {thorny_guild.currency.emoji}{item.item_cost}\n"
                          f"**Your Balance:** {thorny_guild.currency.emoji}{thorny_user.balance}\n\n"
                          f"**You can have maximum** {item.item_max_count} of `{item.item_display_name}`\n"
                          f"**You currently have** {item.item_count} of `{item.item_display_name}`\n")

    return embed

def store_receipt(thorny_user: user.User, thorny_guild: guild.Guild, history: dict):
    embed = discord.Embed(colour=0xFFBF00,
                          title="Receipt")

    if len(history) > 0:
        receipt_text = ""
        for key, value in history.items():
            receipt_text = f"{receipt_text}x{value} {key}\n"
    else:
        receipt_text = "You bought nothing this session"

    embed.add_field(name="Your Shopping Session:",
                    value=receipt_text)

    return embed

def secret_santa_message(gift_receiver: user.User, request: str):
    embed = discord.Embed(color=0xD70040)

    embed.add_field(name="**Secret Santa**",
                    value=f"Thank you for participating in this year's Secret Santa!\n"
                          f"You are to give a gift to {gift_receiver.discord_member.mention}! "
                          f"(That's `{gift_receiver.username}` in case you can't see the user's @)\n\n"
                          f"To help you pick the perfect gift, here is what they asked for: **{request}.** "
                          f"You don't have to get them exactly that, it just serves as an idea of what you *could* get :))\n\n"
                          f"`Delivery date:` by <t:1672441140:f>\n"
                          f"`Delivery location:` At the spawn Christmas Tree\n"
                          f"`Instructions:` Label the chest with the person's name. Run </delivered:0> in discord when you "
                          f"deliver the gift.")

    return embed

def roa_embed():
    embed = discord.Embed(color=0xD70040,
                          title="Authenticate your Realm or Server")

    embed.add_field(name="<:_pink:921708790322192396> Instructions for Owners",
                    value=f"<:_yellow:921708790313791529> Send an image of your Realm settings as shown in the gif below.\n"
                          f"<:_yellow:921708790313791529> You must then **Copy** the image **link** by pressing the 'Copy Link' "
                          f"button.\n"
                          f"<:_yellow:921708790313791529> Then, click the green `Authenticate` button and paste the image link\n"
                          f"\nNOTE: Please ensure that your Xbox account is connected to Discord. "
                          f"You will not be verified otherwise.")
    embed.add_field(name="<:_pink:921708790322192396> Instructions for Moderators/Admins",
                    value="<:_yellow:921708790313791529> Please ask your **Owner** to confirm your position as Realm Moderator "
                          "or Admin with us. "
                          "It is best if your Owner DM's a ROA Admin.\n"
                          "<:_yellow:921708790313791529> We will then manually verify you.",
                    inline=False)
    embed.add_field(name="Note",
                    value="If you run a Minecraft BDS (Bedrock Dedicated Server), please DM an admin for manual verification.",
                    inline=False)

    embed.set_image(url="https://i.imgur.com/AZPvDjE.gif")

    return embed

def roa_panel(thorny_user: user.User, image: str):
    embed = discord.Embed(color=0xFDDA0D,
                          title=f"Authentication Request")
    embed.add_field(name="Request sent by:",
                    value=f"<@{thorny_user.user_id}>",
                    inline=False)

    embed.add_field(name="Instructions:",
                    value=f"1. Check that the user has their Xbox account is connected to Discord.\n"
                          f"2. Ensure the Xbox account is the same as in the image.\n"
                          f"3. Verify the authenticity of the image.\n\n"
                          f"**Note** that pressing `Deny & Kick` will kick the member from the server and they will have to "
                          f"join again.",
                    inline=False)

    embed.set_image(url=image)
    embed.set_footer(text=thorny_user.user_id)

    return embed
