import discord
import json

from datetime import datetime, timedelta
from thorny_core.db import user
import thorny_core.dbutils as dbutils

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


async def profile_main_embed(thorny_user: user.User, is_donator) -> discord.Embed:
    main_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan or thorny_user.profile.default_slogan}",
                                    color=thorny_user.discord_member.color)
    main_page_embed.set_author(name=thorny_user.discord_member, icon_url=thorny_user.discord_member.display_avatar.url)
    main_page_embed.set_thumbnail(url=thorny_user.discord_member.display_avatar.url)

    profile = thorny_user.profile
    last_month = (datetime.now() - timedelta(days=30)).strftime('%B')
    two_months_ago = (datetime.now() - timedelta(days=60)).strftime('%B')

    main_page_embed.add_field(name=f"**:card_index: Information**",
                              value=f"{is_donator}\n"
                                    f"**Gamertag:** {profile.gamertag or profile.default_gamertag}\n"
                                    f"**Level:** {thorny_user.level.level}\n"
                                    f"**Balance:** <:Nug:884320353202081833> {thorny_user.balance}\n"
                                    f"**Birthday:** {thorny_user.birthday}\n"
                                    f"**Age:** {thorny_user.age}\n"
                                    f"**Joined on:** {thorny_user.join_date}"
                              )

    main_page_embed.add_field(name=f"**:clock8: Quick Stats**",
                              value=f"**Latest Playtime:** {thorny_user.playtime.recent_session}\n"
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

    last_month = (datetime.now() - timedelta(days=30)).strftime('%B')
    two_months_ago = (datetime.now() - timedelta(days=60)).strftime('%B')

    playtime_leaderboard = dbutils.Leaderboard()
    await playtime_leaderboard.select_activity(thorny_user, datetime.now())
    rank = [playtime_leaderboard.activity_list.index(x) + 1 for x in playtime_leaderboard.activity_list if x['user_id'] == thorny_user.user_id][0]

    stats_page_embed.add_field(name=f"**:clock8: Monthly Hours**",
                               value=f"**{datetime.now().strftime('%B')}:** {thorny_user.playtime.current_playtime}\n"
                                     f"**{last_month}:** {thorny_user.playtime.previous_playtime}\n"
                                     f"**{two_months_ago}:** {thorny_user.playtime.expiring_playtime}\n"
                                     f"**Total:** {thorny_user.playtime.total_playtime}\n",
                               inline=True)

    stats_page_embed.add_field(name=f"**:clock8: Today's Roundup**",
                               value=f"You played for **{thorny_user.playtime.todays_playtime}** today\n"
                                     f"You are #{rank} on {datetime.now().strftime('%B')}'s Leaderboard\n",
                               inline=True)

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
                               f"<:arrow_pink:921704277737619476> The Main Page, all about **YOU**\n"
                               f"<:arrow_purple:921704277733425194> The Lore Page, all about your character\n"
                               f"<:arrow_orange:921704277599211540> The Playtime Stats Page, which gives deep insight\n"
                               f"\nAnd so, the **Editing Menus** are split up just the same!\n"
                               f"You have 3 **select Menus** to choose from, for each of the 3 **pages**!\n\n"
                               f"**Now, just choose a section from the menus below and start editing!**")

    return edit_embed
