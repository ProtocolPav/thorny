import discord
import json

from datetime import datetime
import time
import giphy_client
import random

from thorny_core import nexus, utils

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


async def profile_main_embed(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild) -> discord.Embed:

    main_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                    color=thorny_user.discord_member.color)
    main_page_embed.set_author(name=thorny_user.discord_member, icon_url=thorny_user.discord_member.display_avatar.url)
    main_page_embed.set_thumbnail(url=thorny_user.discord_member.display_avatar.url)

    profile = thorny_user.profile

    if thorny_user.birthday:
        today = datetime.now()
        age = today.year - thorny_user.birthday.year - (
                    (today.month, today.day) < (thorny_user.birthday.month, thorny_user.birthday.day))
    else:
        age = 0

    main_page_embed.add_field(name=f"**:card_index: Information**",
                              value=f"**Gamertag:** {thorny_user.gamertag}\n"
                                    f"**Level:** {thorny_user.level}\n"
                                    f"**Balance:** {thorny_guild.currency_emoji} {thorny_user.balance}\n"
                                    f"**Birthday:** {utils.datetime_to_string(thorny_user.birthday)}\n"
                                    f"**Age:** {age}\n"
                                    f"**Joined on:** {utils.datetime_to_string(thorny_user.join_date)}"
                              )

    playtime = thorny_user.playtime

    second_month = datetime.now().replace(month=datetime.now().month-1).strftime('%B')
    third_month = datetime.now().replace(month=datetime.now().month-2).strftime('%B')

    main_page_embed.add_field(name=f"**:clock8: Quick Stats**",
                              value=f"**Today:** {utils.datetime_to_string(playtime.today)}\n"
                                    f"**{datetime.now().strftime('%B')}:** {utils.datetime_to_string(playtime.current_month)}\n"
                                    f"**{second_month}:** {utils.datetime_to_string(playtime.second_month)}\n"
                                    f"**{third_month}:** {utils.datetime_to_string(playtime.third_month)}\n"
                                    f"**Total:** {utils.datetime_to_string(thorny_user.playtime.total)}\n",
                              inline=True)

    main_page_embed.add_field(name=f"**:person_raising_hand: About Me**",
                              value=f'"{profile.aboutme}"',
                              inline=False)

    return main_page_embed


async def profile_lore_embed(thorny_user: nexus.ThornyUser) -> discord.Embed:
    lore_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
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

    return lore_page_embed


async def profile_stats_embed(thorny_user: nexus.ThornyUser) -> discord.Embed:
    stats_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                     color=thorny_user.discord_member.color)

    stats_page_embed.set_author(name=thorny_user.discord_member,
                                icon_url=thorny_user.discord_member.display_avatar.url)

    interactions = await thorny_user.interactions.build(thorny_user.thorny_id)

    blocks_mined = []
    for block in interactions.blocks_mined:
        if len(blocks_mined) == 3:
            break
        else:
            blocks_mined.append(f'**{block.reference}:** {block.count:,}')

    mined_text = '\n'.join(blocks_mined)

    blocks_placed = []
    for block in interactions.blocks_placed:
        if len(blocks_placed) == 3:
            break
        else:
            blocks_placed.append(f'**{block.reference}:** {block.count:,}')

    placed_text = '\n'.join(blocks_placed)

    stats_page_embed.add_field(name=f"**<:Gatherer:997595498963800145> Blocks Mined**",
                               value=f"{mined_text}\n"
                                     f"**Total:** "
                                     f"{interactions.totals['mine'] if interactions.totals['mine'] else 0:,}",
                               inline=True)

    stats_page_embed.add_field(name=f"**<:grassblock:1222769432774840340> Blocks Placed**",
                               value=f"{placed_text}\n"
                                     f"**Total:** " 
                                     f"{interactions.totals['place'] if interactions.totals['place'] else 0:,}",
                               inline=True)

    stats_page_embed.add_field(name=f"\t",
                               value=f"\t")

    stats_page_embed.add_field(name=f"**<:Knight:997595500901568574> Kills**",
                               value=f"**Total Kills:** " 
                                     f"{interactions.totals['kill'] if interactions.totals['kill'] else 0:,}",
                               inline=True)

    stats_page_embed.add_field(name=f"**:skull: Deaths**",
                               value=f"**Total Deaths:** " 
                                     f"{interactions.totals['die'] if interactions.totals['die'] else 0:,}",
                               inline=True)

    stats_page_embed.add_field(name=f"\t",
                               value=f"\t")

    return stats_page_embed


async def profile_edit_embed(thorny_user: nexus.ThornyUser) -> discord.Embed:
    edit_embed = discord.Embed(title="Editing Your Profile",
                               colour=thorny_user.discord_member.colour)

    edit_embed.add_field(name="It's simple. No, really!",
                         value=f"You can edit 2 pages of your profile:\n"
                               f"- The Main Page, all about **YOU**\n"
                               f"- The Lore Page, all about your character\n\n"
                               f"To start editing, just select something from the **Select Menus** "
                               f"and start editing!")

    return edit_embed


def project_application_builder_embed(thorny_user: nexus.ThornyUser, project: ...) -> discord.Embed:
    embed = discord.Embed(title="Project Application Builder",
                          colour=0xFDDA0D)
    embed.set_author(name=thorny_user.username,
                     icon_url=thorny_user.discord_member.display_avatar.url)

    embed.add_field(name="Project Info:",
                    value=f"**Name:** `{project.name or '[EMPTY]'}`\n"
                          f"**Coordinates:** `{project.coordinates or '[EMPTY]'}`\n"
                          f"**Road Built:** `{project.road_built or '[EMPTY]'}`")

    embed.add_field(name="Project Members:",
                    value=f"{project.members or '`[Enter any Project Members if you have any. If not, leave this blank!]`'}",
                    inline=False)

    embed.add_field(name="Project Description:",
                    value=f"`{project.description or '[Talk in detail about your project.]'}`",
                    inline=False)

    embed.add_field(name="Time Estimation:",
                    value=f"`{project.time_estimation or '[How long do you estimate the project to take?]'}`",
                    inline=False)

    embed.add_field(name=":page_facing_up: How To Submit Your Application",
                    value="Press **Start** to start filling in the project. You will be guided through every part of it.\n"
                          "At the end, a green **Confirm Submission** button will appear. You must press it!",
                    inline=False)

    return embed


def project_application_embed(project: ..., thorny_user: nexus.ThornyUser) -> discord.Embed:
    info_embed = discord.Embed(title=f"{project.name}",
                               colour=0xFDDA0D)
    info_embed.set_author(name=thorny_user.username,
                          icon_url=thorny_user.discord_member.display_avatar.url)

    info_embed.add_field(name="Project Info:",
                         value=f"**Coordinates:** {project.coordinates}\n"
                               f"**Road Built:** {project.road_built}\n"
                               f"**Project Members:** {thorny_user.discord_member.name}, {project.members}")

    info_embed.add_field(name="Project Idea & Time Estimation:",
                         value=f"**Description:** {project.description}\n"
                               f"**Time Estimation:** {project.time_estimation}",
                         inline=False)

    info_embed.add_field(name="CM Comments:",
                         value="A CM will write any reason for Accepting, Denying or placing on a Waiting List here.",
                         inline=False)

    info_embed.add_field(name="**STATUS**",
                         value="IN REVIEW...",
                         inline=False)

    info_embed.set_footer(text=f"{thorny_user.thorny_id}PR{project.project_id}")

    return info_embed


def project_embed(project: ...) -> discord.Embed:
    wiki_page = f"https://everthorn.fandom.com/wiki/{project.name.replace(' ', '_')}"

    info_embed = discord.Embed(title=f"{project.name}",
                               colour=0x50C878)

    info_embed.add_field(name=f"ℹ️ About {project.name}",
                         value=f"{project.description}",
                         inline=False)

    info_embed.add_field(name="🔎 Quick Info",
                         value=f"[{project.name}'s Wiki Page]({wiki_page})\n"
                               f"**Coordinates:** {project.coordinates}\n"
                               f"**Road Built:** {project.road_built}\n"
                               f"**Project Members:** {project.owner.discord_member.name}, {project.members}",
                         inline=False)

    info_embed.add_field(name="📟 Recent Updates",
                         value=f"**Progress Updates are coming to the next Thorny Version.**",
                         inline=False)

    return info_embed


def configure_embed(thorny_guild: nexus.ThornyGuild) -> dict[str, discord.Embed]:
    feature_embed = discord.Embed(title="Configuring Thorny Modules",
                                  colour=0xD7E99A)
    # TODO: Make the features embed
    modules = '\n'.join(thorny_guild.features)
    feature_embed.add_field(name="Current Enabled Modules",
                            value=f"{modules}",
                            inline=False)

    welcome_embed = discord.Embed(title="Configuring Welcome Settings",
                                  colour=0xD7E99A)
    welcome_embed.add_field(name="Current Settings",
                            value=f"**Join, Leave and Birthday Messages Channel:** <#{thorny_guild.channels.get_channel('welcome')}>\n\n"
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
                         value=f"**Logs channel:** <#{thorny_guild.channels.get_channel('logs')}>")
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
                            value=f"**Thorny updates channel:** <#{thorny_guild.channels.get_channel('thorny_updates')}>",
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
                          value=f"**Gulag Channel:** <#{thorny_guild.channels.get_channel('gulag')}>\n"
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


def level_up_embed(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild) -> discord.Embed:
    api_response = api_instance.gifs_search_get(giphy_token, f"{thorny_user.level}", limit=10)
    gifs_list = list(api_response.data)
    gif = random.choice(gifs_list)

    embed = discord.Embed(colour=thorny_user.discord_member.colour)
    embed.set_author(name=thorny_user.username,
                     icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f":partying_face: Congrats!",
                    value=f"You leveled up to **Level {thorny_user.level}!**\n"
                          f"{thorny_guild.level_up_message}")
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


def user_join(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild):
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


def user_leave(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild):
    embed = discord.Embed(colour=0xc34184)
    embed.add_field(name=f"**{thorny_user.username} has left**",
                    value=f"{thorny_guild.leave_message}")

    return embed


def balance_embed(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild):
    embed = discord.Embed(color=0xE0115F)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f'**Financials:**',
                    value=f"**Personal Balance:** {thorny_guild.currency.emoji}{thorny_user.balance}")

    return embed


def balance_edit_embed(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild, amount: int):
    embed = discord.Embed(color=0x7CFC00)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f"Successfully {'Added' if amount > 0 else 'Removed'} {abs(amount)} {thorny_guild.currency.name}",
                    value=f"Balance was **{thorny_guild.currency.emoji}{thorny_user.balance - amount}**\n"
                          f"Balance is now **{thorny_guild.currency.emoji}{thorny_user.balance}**")

    return embed


def payment_embed(thorny_user: nexus.ThornyUser, receivable: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild, amount: int, reason: str):
    embed = discord.Embed(color=0xF4C430)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f'{thorny_guild.currency.emoji} Payment Successful!',
                    value=f'**Amount paid:** {thorny_guild.currency.emoji}{amount}\n'
                          f'**Paid to:** {receivable.discord_member.mention}\n\n'
                          f'**Reason:** {reason}')
    embed.set_footer(text=f"Your balance: {thorny_user.balance} | {receivable.username}'s balance: {receivable.balance}")

    return embed


def transaction_log(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild, transaction_type: str, amount: int, reason: str,
                    time: datetime):
    embed = discord.Embed(color=0xF4C430)
    embed.add_field(name=f"**Transaction - {transaction_type}**",
                    value=f"**ThornyUser:** <@{thorny_user.discord_member.id}>\n"
                          f"**Amount:** {thorny_guild.currency.emoji}{amount}\n"
                          f"**Reason:** {reason}")
    embed.set_footer(text=f"{time}")

    return embed


def store_items(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild):
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


def store_selected_item(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild, item_id: str):
    embed = discord.Embed(colour=0xFFBF00,
                          title="Shop Catalogue")

    item = thorny_user.inventory.get_item(item_id)

    embed.add_field(name=f"**About {item.item_display_name}**",
                    value=f"```{item.description}```\n"
                          f"**Cost:** {thorny_guild.currency.emoji}{item.item_cost}\n"
                          f"**Your Balance:** {thorny_guild.currency.emoji}{thorny_user.balance}\n\n"
                          f"**You can have maximum** {item.item_max_count} of `{item.item_display_name}`\n"
                          f"**You currently have** {item.item_count} of `{item.item_display_name}`\n")

    return embed

def store_receipt(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild, history: dict):
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

def secret_santa_message(gift_receiver: nexus.ThornyUser, request: str):
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


def roa_panel(thorny_user: nexus.ThornyUser, image: str):
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


def connect_embed(time: datetime, thorny_user: nexus.ThornyUser):
    timestamp = round(time.timestamp())

    embed = discord.Embed(title='Player Connected', colour=0x44ef56)

    embed.add_field(name='Details:',
                    value=f"**Gamertag:** {thorny_user.profile.whitelisted_gamertag}\n"
                          f"**System Time:** {time}\n"
                          f"**Your Time:** <t:{timestamp}:D> at <t:{timestamp}:T>")

    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)

    return embed


def disconnect_embed(time: datetime, thorny_user: nexus.ThornyUser):
    timestamp = round(time.timestamp())

    embed = discord.Embed(title='Player Disconnected', colour=0xA52A2A)

    embed.add_field(name='Details:',
                    value=f"**Gamertag:** {thorny_user.profile.whitelisted_gamertag}\n"
                          f"**System Time:** {time}\n"
                          f"**Your Time:** <t:{timestamp}:D> at <t:{timestamp}:T>")

    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)

    return embed


def server_start_embed():
    embed = discord.Embed(colour=0x44ef56)

    embed.add_field(name='The Server is Running',
                    value=f"The server has successfully started! You may now join.")

    return embed


def server_stop_embed():
    embed = discord.Embed(colour=0xA52A2A)

    embed.add_field(name='The Server is Stopped',
                    value=f"I have successfully stopped the server")

    return embed


def server_update_embed(update_version: str):
    embed = discord.Embed(colour=0xFDDA0D)

    embed.add_field(name='Update Found!',
                    value=f"I have found an update to the server: **{update_version}**\n"
                          f"The server has been updated and successfully started. You may now join.")

    return embed


def server_status(online: bool, status: str, uptime: str, load: dict, online_players: dict, everthorn_guilds: bool):
    embed = discord.Embed(color=0x6495ED)

    if everthorn_guilds:
        in_game_days = datetime.now() - datetime.strptime("2022-07-30 16:00", "%Y-%m-%d %H:%M")

        if status == "system_clearance":
            embed.title = f":stopwatch: Restart in 60s || Day {in_game_days.days + 1}"

        elif status == "executing_restart":
            embed.title = f":star2: Regular Restart in progress... || Day {in_game_days.days + 1}"

        elif status == "server_crashed":
            embed.title = f":bangbang: The server has crashed! || Day {in_game_days.days + 1}"

        elif status == "responding_to_crash":
            embed.title = f":star2: Responding to crash... || Day {in_game_days.days + 1}"

        elif online:
            embed.title = f":green_circle: The server is online || Day {in_game_days.days + 1}"

        else:
            embed.title = f":red_circle: The server is offline || Day {in_game_days.days + 1}"

        embed.description = f"**Uptime:** {uptime.split('.')[0] if online else '0:00:00'}\n" \
                            f"**RAM/CPU Usage:** {load['ram_percentage']}% / {load['cpu_percent']}%\n"

    online_text = ''
    for player in online_players:
        time = datetime.now() - player['connect_time']
        time = str(time).split(":")
        online_text = f"{online_text}\n" \
                      f"<@{player['user_id']}> • " \
                      f"connected {time[0]}h{time[1]}m ago"

    if online_text == "":
        embed.add_field(name="**Empty!**",
                        value="*Seems like nobody's online. Perfect time to pull a prank on somebody!*", inline=False)

    elif online_text != "":
        embed.add_field(name="**Connected Players**\n",
                        value=online_text, inline=False)

    return embed


def quests_overview(quests: list[...]):
    embed = discord.Embed(colour=0xE0B0FF,
                          title="Available Quests",
                          description="To see more details about a certain quest, select it in the selector!")

    TEXTLIMIT = 50

    for quest in quests:
        if len(quest.description) > TEXTLIMIT:
            description = f'{quest.description[0:TEXTLIMIT]}...'
        else:
            description = quest.description

        embed.add_field(name=quest.title,
                        value=f"```{description}```",
                        inline=False)

    if len(quests) == 0:
        embed.add_field(name='No quests available!',
                        value=f"Quests usually get refreshed every week, so check back in a bit to see new ones!",
                        inline=False)

    return embed


def quests_admin_overview(quests: list[...]):
    embed = discord.Embed(colour=0xE0B0FF,
                          title="Manage Quests",
                          description="To manage a specific quest, select it in the selector.\n"
                                      "For now you can only Expire a specific quest.")

    TEXTLIMIT = 50

    for quest in quests:
        embed.add_field(name=quest.title,
                        value=f"```{quest.objective_type} {quest.objective}```",
                        inline=False)

    if len(quests) == 0:
        embed.add_field(name='All quests are expired!',
                        value=f"You must create new quests! New quests should be created every Friday.",
                        inline=False)

    return embed


def view_quest(quest: ..., money_symbol: str):
    times = quest.end - datetime.now()
    embed = discord.Embed(colour=0xE0B0FF,
                          title=quest.title,
                          description=f"*This quest will become unavailable <t:{int(time.time() + times.total_seconds())}:R>. "
                                      f"Accept it before time runs out!*")

    embed.add_field(name='🔖 Description',
                    value=f"```{quest.description}```",
                    inline=False)
    embed.add_field(name='🎯 Objective',
                    value=quest.get_objective(),
                    inline=False)
    embed.add_field(name='💎 Rewards',
                    value=quest.get_rewards(money_symbol),
                    inline=False)

    return embed


def quest_progress(quest: ..., money_symbol: str):
    embed = discord.Embed(colour=0xE0B0FF,
                          title=quest.title)

    time_left =''
    if quest.timer and quest.started_on:
        subtraction = datetime.now().replace(microsecond=0) - quest.started_on.replace(microsecond=0)
        time_left = f"\n**Time Left:** {quest.timer - subtraction}"
    elif quest.timer and not quest.started_on:
        time_left = (f"\n**Time Left:** {quest.timer}\n"
                     f"*Timer starts when you start the quest. e.g when you kill your first mob*")

    embed.add_field(name='🔖 Description',
                    value=f"```{quest.description}```",
                    inline=False)
    embed.add_field(name='🎯 Objective',
                    value=quest.get_objective(),
                    inline=False)
    embed.add_field(name='⏱️ Progress',
                    value=f"{quest.completion_count}/{quest.objective_count}{time_left}"
                          f"",
                    inline=False)
    embed.add_field(name='💎 Rewards',
                    value=quest.get_rewards(money_symbol),
                    inline=False)

    return embed
