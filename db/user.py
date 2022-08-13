import asyncpg as pg
from datetime import datetime, timedelta
import discord
from thorny_core import errors
from dataclasses import dataclass, field


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
    role: str = None
    aboutme: str = None
    lore: str = None
    information_shown: bool = True
    aboutme_shown: bool = True
    activity_shown: bool = True
    lore_shown: bool = True

    def __init__(self, profile_data, column_data):
        self.column_data = column_data
        self.slogan = profile_data['slogan']
        self.gamertag = profile_data['gamertag']
        self.role = profile_data['role']
        self.aboutme = profile_data['aboutme']
        self.lore = profile_data['lore']
        self.information_shown = profile_data['information_shown']
        self.activity_shown = profile_data['activity_shown']
        self.lore_shown = profile_data['lore_shown']

    def update(self, attribute, value=None, toggle=False):
        if toggle:
            attr_to_toggle = self.__getattribute__(attribute)
            self.__setattr__(attribute, not attr_to_toggle)
        else:
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
    total_playtime: timedelta = None
    current_playtime: timedelta = None
    previous_playtime: timedelta = None
    expiring_playtime: timedelta = None
    recent_session: timedelta = None
    daily_average: timedelta = None
    session_average: timedelta = None

    def __init__(self, playtime_data, latest_playtime, daily_average):
        self.total_playtime = playtime_data['total_playtime']
        self.current_playtime = playtime_data['current_playtime']
        self.previous_playtime = playtime_data['previous_playtime']
        self.expiring_playtime = playtime_data['expiring_playtime']
        self.recent_session = latest_playtime['playtime']
        self.daily_average = daily_average['averages']


@dataclass
class InventorySlot:
    inventory_id: int
    item_id: str
    item_display_name: str
    item_count: int
    item_max_count: int
    item_cost: int
    redeemable: bool

    def __init__(self, slot):
        self.inventory_id = slot['inventory_id']
        self.item_id = slot['item_id']
        self.item_count = slot['item_count']
        self.item_display_name = slot['display_name']
        self.item_max_count = slot['max_item_count']
        self.item_cost = slot['item_cost']
        self.redeemable = slot['redeemable']


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
                "item_count": None,
                "display_name": item["display_name"],
                "max_item_count": item["max_item_count"],
                "item_cost": item["item_cost"],
                "redeemable": item["redeemable"]
            }
            self.all_items.append(InventorySlot(slot))

    def fetch(self, item_id):
        item_in_inventory = False
        for item in self.slots:
            if item.item_id == item_id:
                item_in_inventory = True
                return item
        if not item_in_inventory:
            for item_data in self.all_items:
                if item_data.item_id == item_id:
                    return item_data

    def data(self, item_id):
        # Delete this soon. I will keep just for the sake of ease for now
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
                    "redeemable": item.redeemable
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
    connection_pool: pg.Pool = field(repr=False)
    discord_member: discord.Member = field(repr=False)
    thorny_id: int
    user_id: int
    guild_id: int
    username: str
    balance: int
    join_date: datetime
    join_date_display: str
    birthday: datetime
    birthday_display: str
    age: int
    profile: Profile
    level: Level
    playtime: Playtime
    inventory: Inventory
    strikes: Strikes
    counters: Counters

    def __init__(self,
                 pool: pg.Pool,
                 member: discord.Member,
                 thorny_user: pg.Record,
                 profile: pg.Record,
                 profile_columns: pg.Record,
                 levels: pg.Record,
                 playtime: pg.Record,
                 recent_playtime: pg.Record,
                 daily_average: pg.Record,
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
        self.user_id = thorny_user['user_id']
        self.balance = thorny_user['balance']
        self.join_date = thorny_user['join_date']
        self.join_date_display = datetime.strftime(self.join_date, "%B %d %Y") if self.join_date is not None \
            else "DM Pav to set up"
        self.birthday = thorny_user['birthday']
        self.birthday_display = datetime.strftime(self.birthday, '%B %d %Y') if self.birthday is not None \
            else "Use `/birthday` to set up!"
        self.age = round((datetime.date(datetime.now()) - self.birthday).days / 365) or None
        self.profile = Profile(profile_data=profile, column_data=profile_columns)
        self.level = Level(level_data=levels)
        self.playtime = Playtime(playtime_data=playtime, latest_playtime=recent_playtime, daily_average=daily_average)
        self.inventory = Inventory(inventory=inventory, item_data=item_data)
        self.strikes = Strikes(strikes=strikes)
        self.counters = Counters(counters=counters)

    async def update(self, attribute, value):
        self.__setattr__(attribute, value)
