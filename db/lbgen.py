from thorny_core.db import user
from datetime import datetime
from dateutil.relativedelta import relativedelta


async def activity_leaderboard(thorny_user: user.User, month: datetime) -> tuple[list, int]:
    user_rank = 0

    async with thorny_user.connection_pool.connection() as conn:
        if datetime.now() < month:
            month = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - relativedelta(years=1)
        else:
            month = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = month + relativedelta(months=1)

        leaderboard = await conn.fetch("""
                                       SELECT SUM(playtime), thorny.user.thorny_user_id, thorny.user.user_id
                                       FROM thorny.activity 
                                       JOIN thorny.user
                                       ON thorny.user.thorny_user_id = thorny.activity.thorny_user_id
                                       WHERE connect_time BETWEEN $1 AND $2
                                            AND playtime IS NOT NULL
                                            AND thorny.user.guild_id = $3 
                                            AND thorny.user.active = True
                                       GROUP BY thorny.user.user_id, thorny.user.thorny_user_id
                                       ORDER BY SUM(playtime) DESC
                                       """,
                                       month, next_month, thorny_user.guild_id)

        for person in leaderboard:
            if person['thorny_user_id'] == thorny_user.thorny_id:
                user_rank = leaderboard.index(person) + 1

    return leaderboard, user_rank


async def money_leaderboard(thorny_user: user.User) -> tuple[list, int]:
    user_rank = 0

    async with thorny_user.connection_pool.connection() as conn:
        leaderboard = await conn.fetch("""
                                       SELECT user_id, thorny_user_id, balance FROM thorny.user
                                       WHERE thorny.user.guild_id = $1
                                       AND thorny.user.active = True
                                       GROUP BY user_id, thorny_user_id, balance
                                       ORDER BY balance DESC
                                       """,
                                       thorny_user.guild_id)

        for person in leaderboard:
            if person['thorny_user_id'] == thorny_user.thorny_id:
                user_rank = leaderboard.index(person) + 1

    return leaderboard, user_rank


async def levels_leaderboard(thorny_user: user.User) -> tuple[list, int]:
    user_rank = 0

    async with thorny_user.connection_pool.connection() as conn:
        leaderboard = await conn.fetch("""
                                       SELECT thorny.user.user_id, thorny.levels.thorny_user_id, user_level
                                       FROM thorny.user 
                                       JOIN thorny.levels 
                                       ON thorny.user.thorny_user_id = thorny.levels.thorny_user_id
                                       WHERE thorny.user.guild_id = $1 
                                       AND thorny.user.active = True
                                       GROUP BY thorny.levels.thorny_user_id, thorny.user.user_id, user_level, xp
                                       ORDER BY xp DESC
                                       """,
                                       thorny_user.guild_id)

        for person in leaderboard:
            if person['thorny_user_id'] == thorny_user.thorny_id:
                user_rank = leaderboard.index(person) + 1

    return leaderboard, user_rank
