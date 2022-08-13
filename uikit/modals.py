import discord
from discord.ui import Modal, InputText
from thorny_core.uikit.slashoptions import profile_sections_select


class ProfileEditModal(Modal):
    def __init__(self, section: str):
        super().__init__(title=f"Editing your Profile...",
                         timeout=120.0)
        placeholder = None
        for option in profile_sections_select:
            if option.label == section:
                placeholder = option.description

        if section == "About Me" or section == "Character Backstory":
            self.add_item(InputText(label=f"Enter your {section}",
                                    style=discord.InputTextStyle.long,
                                    max_length=300,
                                    placeholder=placeholder))
        elif section == "Character Data: Name, Age, Race":
            self.add_item(InputText(label=f"Enter your Character Name",
                                    style=discord.InputTextStyle.short,
                                    placeholder="Think of a unique name for your lore character!"))

            self.add_item(InputText(label=f"Enter your Character Age",
                                    style=discord.InputTextStyle.short,
                                    placeholder="How old is your character?",
                                    required=False))

            self.add_item(InputText(label=f"Enter your Character Race",
                                    style=discord.InputTextStyle.short,
                                    placeholder="Some races include: Human, Elf, Dwarf, etc.",
                                    required=False))

        elif section == "Character Data: Role, Culture, Religion":
            self.add_item(InputText(label=f"Enter your Character Role",
                                    style=discord.InputTextStyle.short,
                                    placeholder="What role do they play in this world?",
                                    required=False))

            self.add_item(InputText(label=f"Enter your Character Culture",
                                    style=discord.InputTextStyle.short,
                                    placeholder="They came from somewhere, so they have some culture to them.",
                                    required=False))

            self.add_item(InputText(label=f"Enter your Character Religion",
                                    style=discord.InputTextStyle.short,
                                    placeholder="Do they follow a religion?",
                                    required=False))

        elif section == "Character Skills: Agility, Valor, Strength":
            self.add_item(InputText(label=f"Enter your Character Agility",
                                    style=discord.InputTextStyle.short,
                                    max_length=1,
                                    placeholder="A number from 1 to 6",
                                    required=False))

            self.add_item(InputText(label=f"Enter your Character Valor",
                                    style=discord.InputTextStyle.short,
                                    max_length=1,
                                    placeholder="A number from 1 to 6",
                                    required=False))

            self.add_item(InputText(label=f"Enter your Character Strength",
                                    style=discord.InputTextStyle.short,
                                    max_length=1,
                                    placeholder="A number from 1 to 6",
                                    required=False))

        elif section == "Character Skills: Charisma, Creativity, Ingenuity":
            self.add_item(InputText(label=f"Enter your Character Charisma",
                                    style=discord.InputTextStyle.short,
                                    max_length=1,
                                    placeholder="A number from 1 to 6",
                                    required=False))

            self.add_item(InputText(label=f"Enter your Character Creativity",
                                    style=discord.InputTextStyle.short,
                                    max_length=1,
                                    placeholder="A number from 1 to 6",
                                    required=False))

            self.add_item(InputText(label=f"Enter your Character Ingenuity",
                                    style=discord.InputTextStyle.short,
                                    max_length=1,
                                    placeholder="A number from 1 to 6",
                                    required=False))
        else:
            self.add_item(InputText(label=f"Enter your {section}",
                                    placeholder=placeholder))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="You entered:", value=self.children[0].value)
        await interaction.response.edit_message(embed=embed)
