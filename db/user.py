from dataclasses import dataclass, field
from datetime import datetime, timedelta, date

import matplotlib.pyplot as plt

import asyncpg as pg
import discord

from thorny_core import errors
from thorny_core.db.guild import Guild
from thorny_core.db.poolwrapper import PoolWrapper


class Time:
    def __init__(self, time_object: datetime | timedelta | date):
        self.time = time_object

    def __str__(self):
        if type(self.time) == (date or datetime):
            datetime_string = datetime.strftime(self.time, "%B %d, %Y")
            return datetime_string
        elif type(self.time) == timedelta:
            total_seconds = int(self.time.total_seconds())
            days, remainder = divmod(total_seconds, 24 * 60 * 60)
            hours, remainder = divmod(remainder, 60*60)
            minutes, seconds = divmod(remainder, 60)

            if days == 0:
                return f"{hours}h{minutes}m"
            elif days == 1:
                return f"{days} day, {hours}h{minutes}m"
            elif days > 1:
                return f"{days} days, {hours}h{minutes}m"

        return str(self.time)


@dataclass
class Profile:
    column_data: pg.Record = field(repr=False)
    default_slogan: str = field(repr=False, default="Your Slogan Goes Here")
    default_gamertag: str = field(repr=False, default="Set Your GT!")
    default_role: str = field(repr=False, default="Wandering Traveler")
    default_aboutme: str = field(repr=False, default="A **REALLY** cool person!")
    default_lore: str = field(repr=False, default="I came from a distant land, far, far away...")
    slogan: str = None
    gamertag: str = None
    aboutme: str = None
    character_name: str = None
    character_age: int = None
    character_race: str = None
    character_role: str = None
    character_origin: str = None
    character_beliefs: str = None
    stats_agility: int = None
    stats_valor: int = None
    stats_strength: int = None
    stats_charisma: int = None
    stats_creativity: int = None
    stats_ingenuity: int = None
    lore: str = None
    information_shown: bool = True
    aboutme_shown: bool = True
    activity_shown: bool = True
    lore_shown: bool = True

    def __init__(self, profile_data, column_data):
        self.column_data = column_data
        self.slogan = profile_data['slogan']
        self.gamertag = profile_data['gamertag']
        self.role = None
        self.aboutme = profile_data['aboutme']
        self.character_name = profile_data['character_name']
        self.character_age = profile_data['character_age']
        self.character_race = profile_data['character_race']
        self.character_role = profile_data['character_role']
        self.character_origin = profile_data['character_origin']
        self.character_beliefs = profile_data['character_beliefs']
        self.agility = profile_data['agility'] if profile_data['agility'] <= 6 else 6
        self.valor = profile_data['valor'] if profile_data['valor'] <= 6 else 6
        self.strength = profile_data['strength'] if profile_data['strength'] <= 6 else 6
        self.charisma = profile_data['charisma'] if profile_data['charisma'] <= 6 else 6
        self.creativity = profile_data['creativity'] if profile_data['creativity'] <= 6 else 6
        self.ingenuity = profile_data['ingenuity'] if profile_data['ingenuity'] <= 6 else 6
        self.lore = profile_data['lore']

    def update(self, attribute, value=None):
        for data in self.column_data:
            if data["column_name"] == str(attribute) and (data["character_maximum_length"] is None or
                                                          data["character_maximum_length"] >= len(value)):
                self.__setattr__(attribute, value)
                break
            elif data["column_name"] == str(attribute) and data["character_maximum_length"] < len(value):
                raise errors.DataTooLongError(len(value), data["character_maximum_length"])


@dataclass
class Level:
    level: int
    xp: int
    required_xp: int

    def __init__(self, level_data):
        self.level = level_data['user_level']
        self.xp = level_data['xp']
        self.required_xp = level_data['required_xp']


@dataclass
class Playtime:
    total_playtime: Time
    current_playtime: Time
    previous_playtime: Time
    expiring_playtime: Time
    todays_playtime: Time
    weekly_ratio: float
    current_connection: pg.Record
    loose_connections: pg.Record
    daily_playtime: pg.Record

    def __init__(self, monthly_data, stats, current_connection, unfulfilled_connections, daily_playtime):
        default = Time(timedelta(hours=0))

        if monthly_data:
            self.current_playtime = Time(monthly_data[0]['playtime'])
            self.previous_playtime = Time(monthly_data[1]['playtime']) if len(monthly_data) >= 2 else default
            self.expiring_playtime = Time(monthly_data[2]['playtime']) if len(monthly_data) >= 3 else default
        else:
            self.current_playtime = default
            self.previous_playtime = default
            self.expiring_playtime = default

        if stats:
            self.total_playtime = Time(stats['total_playtime']) if stats['total_playtime'] is not None else default
            self.todays_playtime = Time(stats['today']) if stats['today'] is not None else default
        else:
            self.total_playtime = default
            self.todays_playtime = default

        self.current_connection = current_connection
        self.loose_connections = unfulfilled_connections
        self.daily_playtime = daily_playtime

        # self.generate_bar_chart()

    def generate_bar_chart(self):
        x_axis = []
        y_axis = []
        print(self.daily_playtime)

        for i in range(0,7):
            day = datetime.today() - timedelta(days=i)
            x_axis.insert(0, f"{day.day}/{day.month}")

            record = self.daily_playtime[i]
            record_day = f"{record['day'].day}/{record['day'].month}"

            print(record, record_day, x_axis[-i])
            if record_day == x_axis[-i]:
                y_axis.insert(0, round(record['playtime'].total_seconds()/3600, 1))
            else:
                y_axis.insert(0, 0)

        plt.bar(x=x_axis, height=y_axis, edgecolor='none')

        ax = plt.axes()
        ax.set_xticks(range(7))
        ax.set_xticklabels(x_axis)
        ax.set_yticklabels([])

        ax.set_axis_bgcolor('dark_grey')

        plt.title('Playtime Graph')
        plt.xlabel('Day')
        plt.ylabel('Hours')
        plt.savefig('pav.png')


@dataclass
class InventorySlot:
    inventory_id: int
    item_id: str
    item_display_name: str
    item_count: int
    item_max_count: int
    item_cost: int
    redeemable: bool
    description: str

    def __init__(self, slot):
        self.inventory_id = slot['inventory_id']
        self.item_id = slot['item_id']
        self.item_count = slot['item_count']
        self.item_display_name = slot['display_name']
        self.item_max_count = slot['max_item_count']
        self.item_cost = slot['item_cost']
        self.redeemable = slot['redeemable']
        self.description = slot['description']


@dataclass
class Inventory:
    original_slots: list[InventorySlot] = field(repr=False)
    all_items: list[InventorySlot] = field(repr=False)
    slots: list[InventorySlot]

    def __init__(self, inventory, item_data):
        self.slots = []
        self.original_slots = []
        self.all_items = []
        for slot in inventory:
            self.slots.append(InventorySlot(slot))
            self.original_slots.append(InventorySlot(slot))
        for item in item_data:
            slot = {
                "inventory_id": None,
                "item_id": item["friendly_id"],
                "item_count": 0,
                "display_name": item["display_name"],
                "max_item_count": item["max_item_count"],
                "item_cost": item["item_cost"],
                "redeemable": item["redeemable"],
                "description": item["description"]
            }
            self.all_items.append(InventorySlot(slot))

    def fetch(self, item_id):
        for item in self.slots:
            if item.item_id == item_id:
                return item

        for item_data in self.all_items:
            if item_data.item_id == item_id:
                return item_data

    def data(self, item_id):
        """Delete this soon. I will keep just for the sake of ease for now
        Replaced with `.fetch()` which fetches either the item in the inventory, or its data if it does not exist."""
        for item_data in self.all_items:
            if item_data.item_id == item_id:
                return item_data

    def add_item(self, item_id, count):
        item = self.fetch(item_id)

        if item.inventory_id is None:
            if item.item_id == item_id and count <= item.item_max_count:
                item_to_add = {
                    "inventory_id": 0,
                    "item_id": item.item_id,
                    "item_count": count,
                    "display_name": item.item_display_name,
                    "max_item_count": item.item_max_count,
                    "item_cost": item.item_cost,
                    "redeemable": item.redeemable,
                    "description": item.description
                }
                self.slots.append(InventorySlot(item_to_add))
            elif count > item.item_max_count:
                raise errors.ItemMaxCountError

        else:
            if item.item_count + count <= item.item_max_count:
                item.item_count += count
            else:
                raise errors.ItemMaxCountError

    def remove_item(self, item_id, count):
        item = self.fetch(item_id)

        if item.inventory_id is None:
            raise errors.MissingItemError
        else:
            if count is None or item.item_count - count <= 0:
                self.slots.remove(item)
            elif item.item_count - count > 0:
                item.item_count -= count

    def __str__(self):
        string = []
        if len(self.slots) > 0:
            for item in self.slots:
                string.append(f"<:_pink:921708790322192396> {item.item_count} **|** {item.item_display_name}\n")
        else:
            string.append("Empty")

        return "".join(string)


@dataclass
class Strike:
    strike_id: int
    manager_id: int
    reason: str

    def __init__(self, strike):
        self.strike_id = strike['strike_id']
        self.manager_id = strike['manager_id']
        self.reason = strike['reason']


@dataclass
class Strikes:
    original_strikes: list[Strike] = field(repr=False)
    strikes: list[Strike]

    def __init__(self, strikes):
        self.strikes = []
        self.original_strikes = []
        for strike in strikes:
            self.strikes.append(Strike(strike))
            self.original_strikes.append(Strike(strike))

    def append(self, manager_id, reason):
        strike = {
            "strike_id": 0,
            "manager_id": manager_id,
            "reason": reason
        }
        self.strikes.append(Strike(strike))

    def soft_remove(self, strike_id):
        strike_found = True
        for strike in self.strikes:
            if strike.strike_id == strike_id:
                strike.reason = f"[FORGIVEN] {strike.reason}"
                strike_found = True
                break
            else:
                strike_found = False
        if not strike_found:
            raise errors.IncorrectStrikeID


@dataclass
class Counters:
    ticket_count: int
    ticket_last_purchase: datetime
    level_last_message: datetime

    def __init__(self, counters):
        for counter in counters:
            if counter['counter_name'] == 'ticket_count':
                self.ticket_count = counter['count']
            elif counter['counter_name'] == 'ticket_last_purchase':
                self.ticket_last_purchase = counter['datetime']
            elif counter['counter_name'] == 'level_last_message':
                self.level_last_message = counter['datetime']


@dataclass
class User:
    connection_pool: PoolWrapper = field(repr=False)
    discord_member: discord.Member = field(repr=False)
    thorny_id: int
    user_id: int
    guild_id: int
    guild: Guild
    username: str
    balance: int
    join_date: Time
    join_date_display: str
    birthday: Time
    birthday_display: str
    age: int
    profile: Profile
    level: Level
    playtime: Playtime
    inventory: Inventory
    strikes: Strikes
    counters: Counters

    def __init__(self,
                 pool: PoolWrapper,
                 member: discord.Member,
                 thorny_user: pg.Record,
                 thorny_guild: Guild,
                 profile: pg.Record,
                 profile_columns: pg.Record,
                 levels: pg.Record,
                 monthly_playtime: pg.Record,
                 daily_playtime: pg.Record,
                 total_playtime: pg.Record,
                 current_connection: pg.Record,
                 unfulfilled_connections: pg.Record,
                 inventory: pg.Record,
                 item_data: pg.Record,
                 strikes: pg.Record,
                 counters: pg.Record
                 ):
        self.connection_pool = pool
        self.discord_member = member
        self.username = self.discord_member.name
        self.thorny_id = thorny_user['thorny_user_id']
        self.guild_id = thorny_user['guild_id']
        self.guild = thorny_guild
        self.user_id = thorny_user['user_id']
        self.balance = thorny_user['balance']
        self.join_date = Time(thorny_user['join_date'])
        self.birthday = Time(thorny_user['birthday'])
        if self.birthday.time is not None:
            today = datetime.now()
            self.age = today.year - self.birthday.time.year - ((today.month, today.day) < (self.birthday.time.month, self.birthday.time.day))
        else:
            self.age = 0
        self.profile = Profile(profile_data=profile, column_data=profile_columns)
        self.level = Level(level_data=levels)
        self.playtime = Playtime(monthly_data=monthly_playtime, stats=total_playtime, current_connection=current_connection,
                                 unfulfilled_connections=unfulfilled_connections, daily_playtime=daily_playtime)
        self.inventory = Inventory(inventory=inventory, item_data=item_data)
        self.strikes = Strikes(strikes=strikes)
        self.counters = Counters(counters=counters)

    async def update(self, attribute, value):
        self.__setattr__(attribute, value)
