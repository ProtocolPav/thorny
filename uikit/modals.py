import discord
from discord.ui import Modal, InputText
from thorny_core.uikit.slashoptions import profile_main_select, profile_lore_select
from thorny_core.db.user import User
from thorny_core.db.commit import commit
import thorny_core.errors as errors


class ProfileEditMain(Modal):
    def __init__(self, section: str, thorny_user: User, embed: discord.Embed):
        super().__init__(title=f"Editing your Profile...",
                         timeout=120.0)
        self.profile_owner = thorny_user
        self.section = section
        self.edit_embed = embed

        placeholder = None
        for option in profile_main_select:
            if option.value == section:
                placeholder = option.description
                self.label = option.label

        if self.label == "About Me":
            self.add_item(InputText(label=f"Enter your {self.label}",
                                    style=discord.InputTextStyle.long,
                                    max_length=300,
                                    placeholder=placeholder))
        else:
            self.add_item(InputText(label=f"Enter your {self.label}",
                                    max_length=40,
                                    placeholder=placeholder))

    async def callback(self, interaction: discord.Interaction):
        self.profile_owner.profile.update(self.section, self.children[0].value)
        await commit(self.profile_owner)
        self.edit_embed.add_field(name=f"You set **{self.label}** to:",
                                  value=self.children[0].value,
                                  inline=False)
        await interaction.response.edit_message(embed=self.edit_embed)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        if isinstance(error, errors.ThornyError):
            await interaction.response.edit_message(embed=error.return_embed())


class ProfileEditLore(Modal):
    def __init__(self, section: str, thorny_user: User, embed: discord.Embed):
        super().__init__(title=f"Editing your Profile...",
                         timeout=120.0)
        self.profile_owner = thorny_user
        self.section = section
        self.edit_embed = embed

        placeholder = None
        for option in profile_lore_select:
            if option.value == section:
                placeholder = option.description
                self.label = option.label

        if self.label == "Character Backstory":
            self.add_item(InputText(label=f"Enter your {self.label}",
                                    style=discord.InputTextStyle.long,
                                    max_length=300,
                                    placeholder=placeholder))
        elif "Character Skills" in self.label:
            self.add_item(InputText(label=f"Enter your {self.label}",
                                    max_length=1,
                                    placeholder=placeholder))
        else:
            self.add_item(InputText(label=f"Enter your {self.label}",
                                    max_length=40,
                                    placeholder=placeholder))

    async def callback(self, interaction: discord.Interaction):
        if "Character Skills" in self.label or "Age" in self.label:
            self.profile_owner.profile.update(self.section, int(self.children[0].value))
        else:
            self.profile_owner.profile.update(self.section, self.children[0].value)
        await commit(self.profile_owner)
        self.edit_embed.add_field(name=f"You set **{self.label}** to:",
                                  value=self.children[0].value,
                                  inline=False)
        await interaction.response.edit_message(embed=self.edit_embed)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        if isinstance(error, errors.ThornyError):
            await interaction.response.edit_message(embed=error.return_embed())

