import discord
from discord.ui import Modal, InputText
from thorny_core.uikit.slashoptions import profile_main_select, profile_lore_select
from thorny_core.uikit.embeds import application_info_embed
from thorny_core.db import User, Guild
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


class ProjectApplicationModal(Modal):
    def __init__(self):
        super().__init__(title="Project Application",
                         timeout=None)

        self.add_item(InputText(label="What is the project name?",
                                placeholder="Eg. Tramonte, Pirate's Cove, Hobbitshire"))
        self.add_item(InputText(label="Type in the coordinates of your project",
                                placeholder="Eg. -400, 233"))
        self.add_item(InputText(label="Have you built a road to your project?",
                                placeholder="If not, when will it be built?"))
        self.add_item(InputText(label="What's your idea? How long will it take?",
                                placeholder="Describe your project. Include a time estimation (eg. 2 months, 1 week)",
                                style=discord.InputTextStyle.long,
                                min_length=100))
        self.add_item(InputText(label="Do you have Project Helpers?",
                                placeholder="List them if you have any. If not, try and get some!"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=None,
                                                content="Thank you for filling in the form!")


class ProjectApplicationExtraInfo(Modal):
    def __init__(self):
        super().__init__(title="Comments",
                         timeout=None)

        self.add_item(InputText(label="Add CM Comments",
                                placeholder="Stuff like the members of the project, and more stuff.",
                                style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()


class ServerEdit(Modal):
    def __init__(self, texts: InputText | list[InputText], thorny_guild: Guild):
        super().__init__(title="Configuring your Server")
        self.thorny_guild = thorny_guild

        if type(texts) == list:
            for text in texts:
                self.add_item(text)
        else:
            self.add_item(texts)

    async def callback(self, interaction: discord.Interaction):
        self.thorny_guild.__setattr__(self.children[0].custom_id, self.children[0].value)
        await commit(self.thorny_guild)
        await interaction.response.defer()


class ServerChannelEdit(Modal):
    def __init__(self, texts: InputText | list[InputText], thorny_guild: Guild):
        super().__init__(title="Editing Channel")
        self.thorny_guild = thorny_guild

        if type(texts) == list:
            for text in texts:
                self.add_item(text)
        else:
            self.add_item(texts)

    async def callback(self, interaction: discord.Interaction):
        self.thorny_guild.channels.__setattr__(self.children[0].custom_id, int(self.children[0].value))
        await commit(self.thorny_guild)
        await interaction.response.defer()


class ServerCurrencyEdit(Modal):
    def __init__(self, texts: InputText | list[InputText], thorny_guild: Guild):
        super().__init__(title="Configuring Currency")
        self.thorny_guild = thorny_guild

        if type(texts) == list:
            for text in texts:
                self.add_item(text)
        else:
            self.add_item(texts)

    async def callback(self, interaction: discord.Interaction):
        self.thorny_guild.currency.__setattr__(self.children[0].custom_id, self.children[0].value)
        await commit(self.thorny_guild)
        await interaction.response.defer()


class RedeemRole(Modal):
    def __init__(self):
        super().__init__(title="Customize Your Role")

        self.add_item(InputText(label="What should your Custom Role be called?",
                                placeholder="Eg. The Champion, Sniffer, Cool Person Role"))
        self.add_item(InputText(label="Enter a Hex Code for the role's colour",
                                placeholder="Eg. #9D5F33"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()


class ROAVerification(Modal):
    def __init__(self):
        super().__init__(title="Enter the link to your image")

        self.add_item(InputText(label="Image link",
                                placeholder="In the form: https://cdn.discordapp.com/attachments/.../link.png"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()