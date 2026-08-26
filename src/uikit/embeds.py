import os
from typing import Optional

import discord
import json

from datetime import UTC, datetime
import time
import giphy_client
import random

from dateutil import relativedelta
from discord import MediaGalleryItem

from nexuscore import AuthenticatedClient
from src import nexus, utils
from src.nexus.guild import OnlineUser
from src.nexus.quest_progress import QuestProgress

version_json = json.load(open('../version.json', 'r'))
v = version_json["version"]
api_instance = giphy_client.DefaultApi()
giphy_token = os.environ.get('GIPHY_TOKEN')


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


async def profile_main_embed(api: AuthenticatedClient, thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild) -> discord.Embed:

    main_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                    color=thorny_user.discord_member.color)
    main_page_embed.set_author(name=thorny_user.discord_member, icon_url=thorny_user.discord_member.display_avatar.url)
    main_page_embed.set_thumbnail(url=thorny_user.discord_member.display_avatar.url)

    profile = thorny_user.profile

    if thorny_user.birthday:
        today = datetime.now(UTC)
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

    playtime = await thorny_user.playtime.build(api, thorny_user.thorny_id)

    second_month = (datetime.now() - relativedelta.relativedelta(months=1)).strftime('%B')
    third_month = (datetime.now() - relativedelta.relativedelta(months=2)).strftime('%B')

    main_page_embed.add_field(name=f"**:clock8: Quick Stats**",
                              value=f"**Today:** {utils.datetime_to_string(playtime.today)}\n"
                                    f"**{datetime.now().strftime('%B')}:** {utils.datetime_to_string(playtime.current_month)}\n"
                                    f"**{second_month}:** {utils.datetime_to_string(playtime.second_month)}\n"
                                    f"**{third_month}:** {utils.datetime_to_string(playtime.third_month)}\n"
                                    f"**Total:** {utils.datetime_to_string(playtime.total)}\n",
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


async def profile_stats_embed(api: AuthenticatedClient, thorny_user: nexus.ThornyUser) -> discord.Embed:
    stats_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                     color=thorny_user.discord_member.color,
                                     description="*Stats shown are from March 7th 2024 onwards*")

    stats_page_embed.set_author(name=thorny_user.discord_member,
                                icon_url=thorny_user.discord_member.display_avatar.url)

    interactions = await thorny_user.interactions.build(api, thorny_user.thorny_id)

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

    kills = []
    for kill in interactions.kills:
        if len(kills) == 3:
            break
        else:
            kills.append(f'**{kill.reference}:** {kill.count:,}')

    kills_text = '\n'.join(kills)

    deaths = []
    for death in interactions.deaths:
        if len(deaths) == 3:
            break
        else:
            deaths.append(f'**{death.reference}:** {death.count:,}')

    deaths_text = '\n'.join(deaths)

    stats_page_embed.add_field(name=f"**<:Miner:1253417396480245852> Blocks Mined**",
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

    stats_page_embed.add_field(name=f"**<:Knight:1253417393494036520> Kills**",
                               value=f"{kills_text}\n"
                                     f"**Total:** "
                                     f"{interactions.totals['kill'] if interactions.totals['kill'] else 0:,}",
                               inline=True)

    stats_page_embed.add_field(name=f"**:skull: Deaths**",
                               value=f"{deaths_text}\n"
                                     f"**Total:** "
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
                          f"**Dimension:** `{project.get('dimension', '[EMPTY]').split('minecraft:')[-1]}`\n"
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
                               f"**Dimension:** {project_data['dimension'].split('minecraft:')[-1]}\n"
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
    wiki_page = f"https://everthorn.net/wiki/{project.project_id}"
    members = [f"<@{x}>" for x in project.members]
    status = f"Project is {project.status.capitalize()}"

    if project.status == 'completed':
        status = f"Project Completed on {utils.datetime_to_string(project.completed_on)}"

    info_embed = discord.Embed(title=f"{project.name}",
                               description=status,
                               colour=0x50C878)

    info_embed.add_field(name=f"ℹ️ About {project.name}",
                         value=f"{project.description}",
                         inline=False)

    info_embed.add_field(name="🔎 Quick Info",
                         value=f"[{project.name}'s Wiki Page]({wiki_page})\n\n"
                               f"**Thread:** <#{project.thread_id}>\n"
                               f"**Started on:** {utils.datetime_to_string(project.started_on)}\n"
                               f"**Coordinates:** {project.coordinates[0]}, {project.coordinates[1]}, {project.coordinates[2]}\n"
                               f"**Dimension:** {project.dimension.split('minecraft:')[-1]}\n"
                               f"**Project Members:** {', '.join(members)}",
                         inline=False)

    return info_embed


def level_up_embed(thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild) -> discord.Embed:
    api_response = api_instance.gifs_search_get(giphy_token, f"{thorny_user.level}", limit=20)
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
    embed.add_field(name=f"**Welcome to {thorny_guild.name}, {thorny_user.username}!**",
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


def user_birthday(thorny_user: nexus.ThornyUser):
    def ordinaltg(n):
        return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

    age = datetime.now(UTC).year - thorny_user.birthday.year

    api_response = api_instance.gifs_search_get(giphy_token, f'{ordinaltg(age)} birthday', limit=10)
    gifs_list = list(api_response.data)
    gif = random.choice(gifs_list)

    embed = discord.Embed(colour=thorny_user.discord_member.colour)
    embed.add_field(name=f"**Happy birthday, {thorny_user.discord_member.nick}!**",
                    value=f"Woooo!!! It's {thorny_user.discord_member.mention}'s {ordinaltg(age)} birthday! Go wish them a big, fat, happy birthday!!!")
    embed.set_image(url=gif.images.original.url)
    embed.set_footer(text=f"The /birthdays command shows you all upcoming birthdays!")

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
    embed = discord.Embed(colour=0x6495ED)

    embed.add_field(name='Server start sent!',
                    value=f"Check the <#1219710096976646175> channel, or the Admin Panel for confirmation")

    return embed


def server_stop_embed():
    embed = discord.Embed(colour=0x6495ED)

    embed.add_field(name='Server stop sent!',
                    value=f"Check the <#1219710096976646175> channel, or the Admin Panel for confirmation")

    return embed


def server_update_embed(update_version: str):
    embed = discord.Embed(colour=0xFDDA0D)

    embed.add_field(name='Update Found!',
                    value=f"I have found an update to the server: **{update_version}**\n"
                          f"The server has been updated and successfully started. You may now join.")

    return embed


def server_status(status: str, start_since: str, online_players: list[OnlineUser], everthorn_guilds: bool):
    embed = discord.Embed(color=0x6495ED)

    if everthorn_guilds:
        in_game_days = datetime.now() - datetime.strptime("2022-07-30 16:00", "%Y-%m-%d %H:%M")
        uptime = datetime.now() - datetime.fromisoformat(start_since)

        if status == "stopped":
            embed.title = f":red_circle: The server is offline || Day {in_game_days.days + 1}"

        else:
            embed.title = f":green_circle: The server is online || Day {in_game_days.days + 1}"

        embed.description = f"**Uptime:** {str(uptime).split('.')[0] if status == 'started' else '0:00:00'}\n" \
                            f"**RAM/CPU Usage:** Not available\n"

    online_text = ''
    for player in online_players:
        time_played = datetime.now(UTC) - player.session
        time_played = str(time_played).split(":")
        online_text = f"{online_text}\n" \
                      f"<@{player.user_id}> • " \
                      f"connected {time_played[0]}h{time_played[1]}m ago"

    if online_text == "":
        embed.add_field(name="**Aha!**",
                        value="*The server is empty. This is the PERFECT time to hop on and prank somebody!*", inline=False)

    elif online_text != "":
        embed.add_field(name="**Connected Players**\n",
                        value=online_text, inline=False)

    return embed


# ─────────────────────────────────────────────────────────────
# Quest embed helpers
# ─────────────────────────────────────────────────────────────

def _quest_type_meta(quest_type: str) -> tuple[str, str]:
    """Returns (emoji, label) for a quest type."""
    match quest_type:
        case 'side':
            return '🏄', 'Side Quest'
        case 'story':
            return '🔖', 'Story Quest'
        case 'weekly':
            return '😄', 'Weekly Quest'
        case _:
            return '⏲️', 'Minor Quest'


def _build_progress_bar(current_index: int, total: int) -> str:
    """
    Returns a coloured square progress bar.
    Completed objectives → green, active → yellow, future → black.
    """
    squares = []
    for i in range(total):
        if i < current_index:
            squares.append('🟩')
        elif i == current_index:
            squares.append('🟨')
        else:
            squares.append('⬛')
    return ''.join(squares)


def _build_sentence(verb: str, parts: list, conjunction: str) -> str:
    if len(parts) == 1:
        return f"**{verb}** {parts[0]}"
    init = ', '.join(parts[:-1])
    last = parts[-1]
    return f"**{verb}** {init}, *{conjunction}* {last}"


def _build_target_lines(objective: 'nexus.quest.Objective',
                        user_objective: 'nexus.quest_progress.ObjectiveProgress' = None) -> str:
    display = getattr(objective, 'display', None)
    if display:
        return f"**{display}**"

    match objective.objective_type:
        case "kill": verb = 'Kill'
        case 'mine': verb = 'Mine'
        case 'visit': verb = 'Locate'
        case _: verb = 'Complete'

    targets = objective.targets

    if not targets:
        return f"**{verb}**..."

    progress_map = {}
    if user_objective is not None:
        progress_map = {tp.target_uuid: tp.count for tp in user_objective.target_progress}

    logic = (objective.logic or 'and').lower()
    target_count = objective.target_count

    def fmt_part(t) -> str:
        name = t.display_name() or verb
        required = t.count
        current = progress_map.get(t.target_uuid, 0)

        if current >= required:
            return f"~~**{required}** {name}~~"

        remaining = required - current
        return f"**{remaining}** {name}"

    # Shared pool: OR with a single cap overriding individual counts
    if logic == 'or' and target_count is not None:
        completed = sum(1 for t in targets if progress_map.get(t.target_uuid, 0) >= t.count)
        names = '/'.join(
            f"~~`{t.display_name() or verb}`~~" if progress_map.get(t.target_uuid, 0) >= t.count
            else f"`{t.display_name() or verb}`"
            for t in targets
        )
        header = f"**{verb}** *any* **{target_count}** *of* {names}"
        if completed >= target_count:
            return f"{header} ✅"
        if completed > 0:
            return f"{header} *({completed}/{target_count} done)*"
        return header

    target_parts = [fmt_part(t) for t in targets]

    if logic == 'and':
        return _build_sentence(verb, target_parts, 'and')
    if logic == 'sequential':
        return _build_sentence(verb, target_parts, 'then') + ' *(in order)*'
    return _build_sentence(verb, target_parts, 'or')

# ─────────────────────────────────────────────────────────────
# Public quest embeds
# ─────────────────────────────────────────────────────────────


def quests_overview(quests: list[nexus.Quest], money_symbol: str):
    embed = discord.Embed(
        colour=0xC9A0DC,
        title='✨ Everthorn Quests',
        description=(
            "🔥 **Quests** are a fun distraction from the Minecraft grind\n"
            "📅 New quests are released **weekly**\n"
            "⏲️ Each quest is only available for a **limited time**\n"
            f"{money_symbol} Nugs & other **rewards** are up for grabs!"
        )
    )

    for quest in quests:
        emoji, quest_type = _quest_type_meta(quest.quest_type)
        times = quest.end_time - datetime.now(UTC)
        tags = [x.capitalize() for x in quest.tags]

        embed.add_field(
            name=f"{emoji}  {quest.title}",
            value=(
                f"> `{'` | `'.join(tags)}`\n"
                f"> \n"
                f"> 💎 **Rewards:** {quest.get_reward_string(money_symbol)}\n"
                f"-# ﹂ {quest_type} · Expires <t:{int(time.time() + times.total_seconds())}:R>"
            ),
            inline=False
        )

    if len(quests) == 0:
        embed.add_field(
            name='No quests available right now',
            value='Quests are refreshed every week — check back soon!',
            inline=False
        )

    return embed


def view_quest(quest: nexus.Quest, money_symbol: str, creator_member: discord.Member):
    times = quest.end_time - datetime.now(UTC)
    tags = [x.capitalize() for x in quest.tags]
    emoji, quest_type = _quest_type_meta(quest.quest_type)

    embed = discord.Embed(
        colour=0xC9A0DC,
        title=quest.title,
        description=f"`{'` | `'.join(tags)}`" if tags else ""
    )

    embed.add_field(
        name='📖 About this Quest',
        value=f"```{quest.description}```",
        inline=False
    )

    embed.add_field(
        name=f'🎯 Objectives',
        value=f'This quest has {len(quest.objectives)} objectives',
        inline=False
    )

    embed.add_field(
        name='💎 Rewards',
        value=quest.get_reward_string(money_symbol),
        inline=True
    )

    embed.add_field(
        name='⏲️ Expires',
        value=f"<t:{int(time.time() + times.total_seconds())}:R>",
        inline=True
    )

    embed.add_field(
        name='',
        value=f"-# {emoji} {quest_type} · Made with ❤️ by {creator_member.mention if creator_member else 'UNKNOWN'}",
        inline=False
    )

    return embed


def quest_progress(quest: nexus.Quest, user_quest: QuestProgress, money_symbol: str) -> Optional[discord.Embed]:
    """
    Generates a Discord embed for the user's current active objective.
    Objectives now support multiple targets; each is shown with individual
    progress matched via target_uuid.
    """
    sorted_objectives = sorted(quest.objectives, key=lambda x: x.order_index)
    total_objectives_count = len(sorted_objectives)

    for index, objective in enumerate(sorted_objectives):
        user_objective = user_quest.get_objective_progress(objective.objective_id)

        if not user_objective:
            continue

        if user_objective.status not in ['active', 'in_progress']:
            continue

        # ── Meta ──────────────────────────────────────────────────
        tags = [x.capitalize() for x in quest.tags]
        emoji, quest_type_label = _quest_type_meta(quest.quest_type)

        # ── Rewards ───────────────────────────────────────────────
        objective_rewards = [
            r.get_reward_display(money_symbol) for r in objective.rewards
        ]

        # ── Progress bar ──────────────────────────────────────────
        progress_bar = _build_progress_bar(index, total_objectives_count)

        # ── Expiry ────────────────────────────────────────────────
        expiry_ts: Optional[int] = None
        if quest.end_time:
            expiry_ts = int(quest.end_time.timestamp())
        elif user_quest.end_time:
            expiry_ts = int(user_quest.end_time.timestamp())

        # ── Extra requirements ────────────────────────────────────
        requirements = objective.get_objective_requirement_string()

        # ── Build embed ───────────────────────────────────────────
        embed = discord.Embed(
            colour=0xC9A0DC,
            title=quest.title,
            description=f"`{'` | `'.join(tags)}`" if tags else ""
        )

        embed.add_field(
            name='🔖 The Story',
            value=f"```{objective.description}```",
            inline=False
        )

        embed.add_field(
            name='🎯 Objective',
            value=objective.display or _build_target_lines(objective, user_objective),
            inline=False
        )

        if requirements:
            embed.add_field(
                name='📋 Extra Requirements',
                value=requirements,
                inline=False
            )

        if objective_rewards:
            embed.add_field(
                name='💎 Objective Rewards',
                value=', '.join(objective_rewards),
                inline=True
            )

        embed.add_field(
            name=f'🎛️ Quest Progress  {index + 1}/{total_objectives_count}',
            value=progress_bar,
            inline=False
        )

        footer_parts = [f"{emoji} {quest_type_label}"]
        if expiry_ts:
            footer_parts.append(f"Expires <t:{expiry_ts}:R>")

        embed.add_field(
            name='',
            value=f"-# {' · '.join(footer_parts)}",
            inline=False
        )

        return embed

    return None


def quest_fail_warn(quest: nexus.Quest):
    embed = discord.Embed(
        colour=0xEC5800,
        title='Admit Your Defeat',
        description=(
            f":bangbang: **THIS QUEST WILL BE GONE FOREVER** :bangbang:\n\n"
            f"Are you sure you want to admit your defeat? "
            f"**{quest.title}** will be ***gone forever*** and you'll lose out on the sweet rewards!"
        )
    )

    return embed


def project_complete_warn():
    embed = discord.Embed(colour=0x00FFFF,
                          title="Mark Project As Complete",
                          description=f"**Are you sure?**\n\n"
                                      f"It's great that you're done with your project, but I just wanna make sure "
                                      f"that you are really, 100% done.\n"
                                      f"**Once you mark a project as complete, you can't undo it!**")

    return embed
