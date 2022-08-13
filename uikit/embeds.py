import discord
import json

from datetime import datetime, timedelta
from thorny_core.db import user

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


def profile_main_embed(thorny_user: user.User, is_donator) -> discord.Embed:
    main_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
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
                                    f"**Birthday:** {thorny_user.birthday_display}\n"
                                    f"**Age:** {thorny_user.age}\n"
                                    f"**Joined on:** {thorny_user.join_date_display}"
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


def profile_lore_embed(thorny_user: user.User) -> discord.Embed:
    lore_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                    color=thorny_user.discord_member.color)

    lore_page_embed.set_author(name=thorny_user.discord_member,
                               icon_url=thorny_user.discord_member.display_avatar.url)
    lore_page_embed.set_thumbnail(url=thorny_user.discord_member.display_avatar.url)

    emoji = "⦿"

    lore_page_embed.add_field(name="My Character",
                              value=f"**Name:** Captain Paul Easton\n"
                                    f"**Age:** 32\n"
                                    f"**Race:** Human\n"
                                    f"**Role:** Captain\n"
                                    f"**Culture:** Pirate Culture\n"
                                    f"**Religion:** None\n"
                              )

    lore_page_embed.add_field(name="Skills",
                              value=f"**Agility:** {emoji*2}\n"
                                    f"**Valor:** {emoji*6}\n"
                                    f"**Strength:** {emoji*1}\n"
                                    f"**Charisma:** {emoji*3}\n"
                                    f"**Creativity:** {emoji*2}\n"
                                    f"**Ingenuity:** {emoji*4}\n"
                              )

    lore_page_embed.add_field(name=f"**:dart: Character Backstory**",
                              value=f'"{thorny_user.profile.lore}"',
                              inline=False)

    lore_page_embed.set_footer(text=f"{v} | Lore")

    return lore_page_embed


def profile_stats_ember(thorny_user: user.User) -> discord.Embed:
    stats_page_embed = discord.Embed(title=f"{thorny_user.profile.slogan}",
                                     color=thorny_user.discord_member.color)

    stats_page_embed.set_author(name=thorny_user.discord_member,
                                icon_url=thorny_user.discord_member.display_avatar.url)

    stats_page_embed.set_footer(text=f"{v} | Playtime Stats")

    return stats_page_embed
