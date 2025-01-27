from datetime import datetime

import discord
from discord.ui import Modal, InputText
from thorny_core.uikit.options import profile_main_select, profile_lore_select
from thorny_core.uikit.embeds import project_application_builder_embed
import thorny_core.thorny_errors as thorny_errors

from thorny_core import nexus

class ProfileEditMain(Modal):
    def __init__(self, section: str, thorny_user: nexus.ThornyUser, embed: discord.Embed):
        super().__init__(title=f"Editing your Profile...",
                         timeout=None)
        self.profile_owner = thorny_user
        self.section = section
        self.edit_embed = embed

        placeholder = None
        for option in profile_main_select():
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
                                    max_length=35,
                                    placeholder=placeholder))

    async def callback(self, interaction: discord.Interaction):
        if self.section == 'gamertag':
            self.profile_owner.__setattr__(self.section, self.children[0].value)
            await self.profile_owner.update()
        elif self.section == 'birthday':
            self.profile_owner.__setattr__(self.section, datetime.strptime(self.children[0].value, '%Y/%m/%d'))
            await self.profile_owner.update()
        else:
            self.profile_owner.profile.__setattr__(self.section, self.children[0].value)
            print(self.profile_owner.profile)
            await self.profile_owner.profile.update()

        self.edit_embed.add_field(name=f"You set **{self.label}** to:",
                                  value=self.children[0].value,
                                  inline=False)

        await interaction.response.edit_message(embed=self.edit_embed)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        if isinstance(error, thorny_errors.ThornyError):
            await interaction.response.edit_message(embed=error.return_embed())


class ProfileEditLore(Modal):
    def __init__(self, section: str, thorny_user: nexus.ThornyUser, embed: discord.Embed):
        super().__init__(title=f"Editing your Profile...",
                         timeout=None)
        self.profile_owner = thorny_user
        self.section = section
        self.edit_embed = embed

        placeholder = None
        for option in profile_lore_select():
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
                                    max_length=35,
                                    placeholder=placeholder))

    async def callback(self, interaction: discord.Interaction):
        if "Character Skills" in self.label or "Age" in self.label:
            self.profile_owner.profile.__setattr__(self.section, int(self.children[0].value))
            await self.profile_owner.profile.update()
        else:
            self.profile_owner.profile.__setattr__(self.section, self.children[0].value)
            await self.profile_owner.profile.update()

        self.edit_embed.add_field(name=f"You set **{self.label}** to:",
                                  value=self.children[0].value,
                                  inline=False)

        await interaction.response.edit_message(embed=self.edit_embed)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        if isinstance(error, thorny_errors.ThornyError):
            await interaction.response.edit_message(embed=error.return_embed())


class ProjectDetailsName(Modal):
    def __init__(self, thorny_user: nexus.ThornyUser, project: dict, view: discord.ui.View):
        super().__init__(title="Pick your Project Name",
                         timeout=None)

        self.thorny_user = thorny_user
        self.project = project
        self.view = view

        self.add_item(InputText(label="What would you like to call your Project?",
                                placeholder="Pick a cool name! You won't be able to change it later."))

    async def callback(self, interaction: discord.Interaction):
        self.project['name'] = self.children[0].value

        button = self.view.children[0]
        button.label = "Next [2/3]"

        await interaction.response.edit_message(embed=project_application_builder_embed(self.thorny_user, self.project),
                                                view=self.view)


class ProjectDetailsCoordinates(Modal):
    def __init__(self, thorny_user: nexus.ThornyUser, project: dict, view: discord.ui.View):
        super().__init__(title="Mark down your Project Coordinates",
                         timeout=None)

        self.thorny_user = thorny_user
        self.project = project
        self.view = view

        self.add_item(InputText(label="Put down ONLY the X coordinate",
                                placeholder="Coordinates in Minecraft are: X, Y, Z"))
        self.add_item(InputText(label="Put down ONLY the Y coordinate",
                                placeholder="Coordinates in Minecraft are: X, Y, Z"))
        self.add_item(InputText(label="Put down ONLY the Z coordinate",
                                placeholder="Coordinates in Minecraft are: X, Y, Z"))

    async def callback(self, interaction: discord.Interaction):
        self.project['coordinates'] = [int(self.children[0].value), int(self.children[1].value), int(self.children[2].value)]

        button = self.view.children[0]
        button.label = "Next [3/3]"

        await interaction.response.edit_message(embed=project_application_builder_embed(self.thorny_user, self.project),
                                                view=self.view)


class ProjectDetailsDescription(Modal):
    def __init__(self, thorny_user: nexus.ThornyUser, project: dict, view: discord.ui.View):
        super().__init__(title="Describe your Project",
                         timeout=None)

        self.thorny_user = thorny_user
        self.project = project
        self.view = view

        self.add_item(InputText(label="What's your project idea?",
                                placeholder="Go into as much detail as possible!",
                                style=discord.InputTextStyle.long,
                                min_length=100, max_length=900))
        self.add_item(InputText(label="How long will the project take you?",
                                placeholder="This is a time estimation (eg. 2 months, 1 week)"))
        self.add_item(InputText(label="Have you built a road to your project?",
                                placeholder="If not, start now!"))

    async def callback(self, interaction: discord.Interaction):
        self.project['description'] = self.children[0].value
        self.project['time_estimation'] = self.children[1].value
        self.project['road_built'] = self.children[2].value

        button = self.view.children[0]
        button.label = "Confirm Submission"
        button.style = discord.ButtonStyle.green

        await interaction.response.edit_message(embed=project_application_builder_embed(self.thorny_user, self.project),
                                                view=self.view)


class ProjectApplicationExtraInfo(Modal):
    def __init__(self, title: str, label: str, placeholder: str):
        super().__init__(title=title,
                         timeout=None)

        self.add_item(InputText(label=label,
                                placeholder=placeholder,
                                style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
