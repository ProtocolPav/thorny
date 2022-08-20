"""
Here are the lists or functions that are used in Thorny slash command options or
Thorny slash command autocomplete
"""
from datetime import datetime
from discord import SelectOption

days = [i for i in range(1, 31)]

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

current_month = datetime.now().strftime("%B")

years = [i for i in range(1980, 2016)]

profile_main_select = [SelectOption(label="Slogan",
                                    value="slogan",
                                    description="The very top part of your Profile. Make it memorable!",
                                    emoji="💬"),
                       SelectOption(label="Gamertag",
                                    value="gamertag",
                                    description="Your in-game gamertag. It is CAP and s p a c e  sensitive.",
                                    emoji="🏷️"),
                       SelectOption(label="About Me",
                                    value="aboutme",
                                    description="A paragraph all about you! Max. 300 characters.",
                                    emoji="🙋")]

profile_lore_select = [SelectOption(label="Character Data: Name",
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
                                    emoji="📜")]

profile_stats_select = [SelectOption(label="Coming soon...",
                                     description="Just gotta wait a bit!",
                                     emoji=None), ]
