"""
Here are the lists or functions that are used in Thorny slash command options or
Thorny slash command autocomplete

UPDATE TO THIS:
Make everything a function which returns the things needed, and rename the file to generators.py
"""
import asyncio
from datetime import datetime
from discord import SelectOption, OptionChoice
from thorny_core.db.poolwrapper import pool_wrapper
from thorny_core.db import User


def current_month():
    return datetime.now().strftime("%B")


def days_of_the_month():
    return [i for i in range(1, 31)]


def all_months():
    return ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def years():
    return [i for i in range(1980, datetime.now().year)]


def profile_main_select():
    return [
            SelectOption(label="Slogan",
                         value="slogan",
                         description="The very top part of your Profile. Make it memorable!",
                         emoji="💬"),
            SelectOption(label="Gamertag",
                         value="gamertag",
                         description="Your in-game gamertag. It is CAP and s p a c e  sensitive.",
                         emoji="🏷️"),
            SelectOption(label="Birthday",
                         value="birthday",
                         description="Your birthday! Let everyone know when it is!",
                         emoji="🎉"),
            SelectOption(label="About Me",
                         value="aboutme",
                         description="A paragraph all about you! Max. 300 characters.",
                         emoji="🙋")
    ]


def profile_lore_select():
    return[
           SelectOption(label="Character Data: Name",
                        value="character_name",
                        description="What name do you want to give your character?",
                        emoji="🪧"),
           SelectOption(label="Character Data: Age",
                        value="character_age",
                        description="How old are they?",
                        emoji="🗓️"),
           SelectOption(label="Character Data: Race",
                        value="character_race",
                        description="Some races include: Human, Elf, Hobbit, Dwarf, etc.",
                        emoji="🧝"),
           SelectOption(label="Character Data: Role",
                        value="character_role",
                        description="Some roles include: Knight, Captain, Mage, etc.",
                        emoji="🧙"),
           SelectOption(label="Character Data: Origin",
                        value="character_origin",
                        description="Where did they come from? Eg. A town, another world.",
                        emoji="🪐"),
           SelectOption(label="Character Data: Beliefs",
                        value="character_beliefs",
                        description="Are they religious? Do they believe in something else?",
                        emoji="☯️"),
           SelectOption(label="Character Skills: Agility",
                        value="agility",
                        description="From 0 to 6.",
                        emoji="🏹"),
           SelectOption(label="Character Skills: Valor",
                        value="valor",
                        description="From 0 to 6.",
                        emoji="🏹"),
           SelectOption(label="Character Skills: Strength",
                        value="strength",
                        description="From 0 to 6.",
                        emoji="🏹"),
           SelectOption(label="Character Skills: Charisma",
                        value="charisma",
                        description="From 0 to 6.",
                        emoji="🏹"),
           SelectOption(label="Character Skills: Creativity",
                        value="creativity",
                        description="From 0 to 6.",
                        emoji="🏹"),
           SelectOption(label="Character Skills: Ingenuity",
                        value="ingenuity",
                        description="From 0 to 6.",
                        emoji="🏹"),
           SelectOption(label="Character Backstory",
                        value="lore",
                        description="Who doesn't love a good character backstory? Max. 300 characters.",
                        emoji="📜")
    ]


def profile_stats_select():
    return [
            SelectOption(label="Coming soon...",
                         description="Just gotta wait a bit!",
                         emoji=None)]


def server_setup():
    return [
            SelectOption(label="Welcome Configuration",
                         value="welcome",
                         description="Edit join/leave and birthday messages & choose where they get sent"),
            SelectOption(label="Level Configuration",
                         value="levels",
                         description="Edit level up messages, XP multipliers or disable levels"),
            SelectOption(label="Logs Configuration",
                         value="logs",
                         description="Choose where logs get sent"),
            SelectOption(label="Thorny Updates",
                         value="updates",
                         description="Choose where Thorny Update messages are sent to"),
            SelectOption(label="Gulag Configuration",
                         value="gulag",
                         description="Create the Gulag Channel & Role"),
            SelectOption(label="Thorny Responses Configuration",
                         value="responses",
                         description="Configure wildcard & exact responses"),
            SelectOption(label="Currency Configuration",
                         value="currency",
                         description="Choose a name & emoji for your currency")
    ]


def shop_items():
    async def get():
        async with pool_wrapper.connection() as conn:
            items = await conn.fetch("""
                                     SELECT * FROM thorny.item_type
                                     WHERE item_cost > 0
                                     """)
            return items

    item_rec = asyncio.get_event_loop().run_until_complete(get())

    return_list = []
    for item in item_rec:
        return_list.append(SelectOption(label=item['display_name'],
                                        value=item['friendly_id'],
                                        description=item['description']))

    return return_list


def slash_command_all_items():
    async def get():
        async with pool_wrapper.connection() as conn:
            items = await conn.fetch("""
                                     SELECT * FROM thorny.item_type
                                     """)
            return items

    item_rec = asyncio.get_event_loop().run_until_complete(get())

    return_list = []
    for item in item_rec:
        return_list.append(OptionChoice(name=item['display_name'],
                                        value=item['friendly_id']))

    return return_list


def redeem_items(thorny_user: User):
    return_list = []
    for item in thorny_user.inventory.slots:
        if item.redeemable:
            return_list.append(SelectOption(label=item.item_display_name,
                                            value=item.item_id,
                                            description=item.description))

    return return_list
