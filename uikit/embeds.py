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


def project_application_builder_embed(thorny_user: nexus.ThornyUser, project: dict) -> discord.Embed:
    embed = discord.Embed(title="Project Application Builder",
                          colour=0xFDDA0D)
    embed.set_author(name=thorny_user.username,
                     icon_url=thorny_user.discord_member.display_avatar.url)

    embed.add_field(name="Project Info:",
                    value=f"**Name:** `{project.get('name', '[EMPTY]')}`\n"
                          f"**Coordinates:** `{project.get('coordinates', '[EMPTY]')}`\n"
                          f"**Road Built:** `{project.get('road_built', '[EMPTY]')}`")

    embed.add_field(name="Project Members:",
                    value=f"{project.get('members', '[EMPTY]')}",
                    inline=False)

    embed.add_field(name="Project Description:",
                    value=f"`{project.get('description', '[EMPTY]')}`",
                    inline=False)

    embed.add_field(name="Time Estimation:",
                    value=f"`{project.get('time_estimation', '[EMPTY]')}`",
                    inline=False)

    embed.add_field(name=":page_facing_up: How To Submit Your Application",
                    value="Press **Start** to start filling in the project. You will be guided through every part of it.\n"
                          "At the end, a green **Confirm Submission** button will appear. You must press it!",
                    inline=False)

    return embed


def project_application_embed(project: nexus.Project, project_data: dict, thorny_user: nexus.ThornyUser) -> discord.Embed:
    info_embed = discord.Embed(title=f"{project.name}",
                               colour=0xFDDA0D)
    info_embed.set_author(name=thorny_user.username,
                          icon_url=thorny_user.discord_member.display_avatar.url)

    info_embed.add_field(name="Project Info:",
                         value=f"**Coordinates:** {project_data['coordinates']}\n"
                               f"**Road Built:** {project_data['road_built']}\n"
                               f"**Project Members:** {thorny_user.discord_member.name}")

    info_embed.add_field(name="Project Idea & Time Estimation:",
                         value=f"**Description:** {project.description}\n"
                               f"**Time Estimation:** {project_data['time_estimation']}",
                         inline=False)

    info_embed.add_field(name="CM Comments:",
                         value="A CM will write any reason for Accepting, Denying or placing on a Waiting List here.",
                         inline=False)

    info_embed.add_field(name="**STATUS**",
                         value="IN REVIEW...",
                         inline=False)

    info_embed.set_footer(text=f"{project.project_id}")

    return info_embed


def project_embed(project: nexus.Project) -> discord.Embed:
    wiki_page = f"https://everthorn.fandom.com/wiki/{project.name.replace(' ', '_')}"

    info_embed = discord.Embed(title=f"{project.name}",
                               colour=0x50C878)

    info_embed.add_field(name=f"ℹ️ About {project.name}",
                         value=f"{project.description}",
                         inline=False)

    info_embed.add_field(name="🔎 Quick Info",
                         value=f"[{project.name}'s Wiki Page]({wiki_page})\n"
                               f"**Coordinates:** {project.coordinates_x}, {project.coordinates_y}, {project.coordinates_z}\n"
                               f"**Project Members:** *Coming Soon!*",
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
                    value=f"**Personal Balance:** {thorny_guild.currency_emoji}{thorny_user.balance}")

    return embed


def balance_edit_embed(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild, amount: int):
    embed = discord.Embed(color=0x7CFC00)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f"Successfully {'Added' if amount > 0 else 'Removed'} {abs(amount)} {thorny_guild.currency_name}",
                    value=f"Balance was **{thorny_guild.currency_emoji}{thorny_user.balance - amount}**\n"
                          f"Balance is now **{thorny_guild.currency_emoji}{thorny_user.balance}**")

    return embed


def payment_embed(thorny_user: nexus.ThornyUser, receivable: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild, amount: int, reason: str):
    embed = discord.Embed(color=0xF4C430)
    embed.set_author(name=thorny_user.username, icon_url=thorny_user.discord_member.display_avatar.url)
    embed.add_field(name=f'{thorny_guild.currency_emoji} Payment Successful!',
                    value=f'**Amount paid:** {thorny_guild.currency_emoji}{amount}\n'
                          f'**Paid to:** {receivable.discord_member.mention}\n\n'
                          f'**Reason:** {reason}')
    embed.set_footer(text=f"Your balance: {thorny_user.balance} | {receivable.username}'s balance: {receivable.balance}")

    return embed


def transaction_log(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild,
                    transaction_type: str, amount: int, reason: str, time: datetime):
    embed = discord.Embed(color=0xF4C430)
    embed.add_field(name=f"**Transaction - {transaction_type}**",
                    value=f"**User:** {thorny_user.discord_member.mention}\n"
                          f"**Amount:** {thorny_guild.currency_emoji}{amount}\n"
                          f"**Reason:** {reason}")
    embed.set_footer(text=f"{time}")

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


def server_status(online: bool, status: str, uptime: str, load: dict, online_players: list[dict], everthorn_guilds: bool):
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
        time = datetime.now() - datetime.strptime(player['session'], "%Y-%m-%d %H:%M:%S.%f")
        time = str(time).split(":")
        online_text = f"{online_text}\n" \
                      f"<@{player['discord_id']}> • " \
                      f"connected {time[0]}h{time[1]}m ago"

    if online_text == "":
        embed.add_field(name="**Aha!**",
                        value="*The server is empty. This is the PERFECT time to hop on and prank somebody!*", inline=False)

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


def view_quest(quest: nexus.Quest, money_symbol: str):
    times = quest.end_time - datetime.now()
    embed = discord.Embed(colour=0xE0B0FF,
                          title=quest.title,
                          description=f"*This quest will become unavailable <t:{int(time.time() + times.total_seconds())}:R>. "
                                      f"Accept it before time runs out!*")

    embed.add_field(name='🔖 Description',
                    value=f"```{quest.description}```",
                    inline=False)

    objective_string = ''
    reward_string = ''
    counter = 1
    for objective in quest.objectives:
        name = objective.objective.split(':')[1].capitalize().replace('_', ' ')
        objective_type = objective.objective_type.capitalize()
        requirements = objective.get_objective_requirement_string()

        objective_rewards = []
        for reward in objective.rewards:
            objective_rewards.append(reward.get_reward_display(money_symbol))

        if not objective_rewards:
            objective_rewards.append("No rewards available")

        reward_string = f'{reward_string}{counter}. {", ".join(objective_rewards)}\n'

        objective_string = f'{objective_string}{counter}. {objective_type} {objective.objective_count} **{name}** {requirements}\n'

        counter += 1

    embed.add_field(name=f':dart: Objectives',
                    value=f'{objective_string}\n',
                    inline=False)

    embed.add_field(name='💎 Rewards',
                    value=f'{reward_string}\n',
                    inline=False)

    embed.add_field(name='⏱️ Notes',
                    value=f"- *Objectives must be completed in order*\n"
                          f"- *Rewards are given after each objective!*\n"
                          f"- *Timers start upon your first block mined or enemy killed*\n"
                          f"- *Failing any objective fails the entire quest!*",
                    inline=False)

    return embed


def quest_progress(quest: nexus.Quest, thorny_user: nexus.ThornyUser, money_symbol: str):
    embed = discord.Embed(colour=0xE0B0FF,
                          title=quest.title)

    embed.add_field(name='🔖 Description',
                    value=f"```{quest.description}```",
                    inline=False)

    objective_string = ''
    reward_string = ''
    counter = 1
    for objective in quest.objectives:
        name = objective.objective.split(':')[1].capitalize().replace('_', ' ')
        objective_type = objective.objective_type.capitalize()
        requirements = objective.get_objective_requirement_string()

        objective_rewards = []
        for reward in objective.rewards:
            objective_rewards.append(reward.get_reward_display(money_symbol))

        if not objective_rewards:
            objective_rewards.append("No rewards available")

        reward_string = f'{reward_string}{counter}. {", ".join(objective_rewards)}\n'

        for user_objective in thorny_user.quest.objectives:
            progress = objective.objective_count - user_objective.completion

            if user_objective.objective_id == objective.objective_id and user_objective.status != 'in_progress':
                objective_string = f'{objective_string}{counter}. ~~{objective_type} {progress} **{name}** {requirements}~~\n'
            elif user_objective.objective_id == objective.objective_id:
                objective_string = f'{objective_string}{counter}. {objective_type} {progress} **{name}** {requirements}\n'

        counter += 1

    embed.add_field(name=f':dart: Objectives',
                    value=f'{objective_string}\n',
                    inline=False)

    embed.add_field(name='💎 Rewards',
                    value=f'{reward_string}\n',
                    inline=False)

    embed.add_field(name='⏱️ Notes',
                    value=f"- *Objectives must be completed in order*\n"
                          f"- *Rewards are given after each objective!*\n"
                          f"- *Timers start upon your first block mined or enemy killed*\n"
                          f"- *Failing any objective fails the entire quest!*",
                    inline=False)

    return embed


def quest_fail_warn(quest: nexus.Quest):
    embed = discord.Embed(colour=0xEC5800,
                          title="Admit Your Defeat",
                          description=f":bangbang: **THIS QUEST WILL BE GONE FOREVER** :bangbang:\n\n"
                                      f"Are you sure you want to admit your defeat? "
                                      f"**{quest.title}** will be ***gone forever*** an you'll lose out on the sweet rewards!")

    return embed
