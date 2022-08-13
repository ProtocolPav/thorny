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

profile_sections_select = [SelectOption(label="Slogan",
                                        description="The very top part of your Profile. Make it memorable!",
                                        emoji="💬"),
                           SelectOption(label="Gamertag",
                                        description="Your in-game gamertag. It is CAP and s p a c e  sensitive.",
                                        emoji="🏷️"),
                           SelectOption(label="About Me",
                                        description="A paragraph all about you! Max. 300 characters.",
                                        emoji="🙋"),
                           SelectOption(label="Character Data: Name, Age, Race",
                                        description="Part of your lore. Your character... They've got a name, right?",
                                        emoji="🧝"),
                           SelectOption(label="Character Data: Role, Culture, Religion",
                                        description="Part of your lore. They must come from somewhere.",
                                        emoji="🏰"),
                           SelectOption(label="Character Skills: Agility, Valor, Strength",
                                        description="Part of your lore. Put values from 1 to 6.",
                                        emoji="💡"),
                           SelectOption(label="Character Skills: Charisma, Creativity, Ingenuity",
                                        description="Part of your lore. Put values from 1 to 6.",
                                        emoji="⚔"),
                           SelectOption(label="Character Backstory",
                                        description="Who doesn't love a good character backstory? Max. 300 characters.",
                                        emoji="📜")]
