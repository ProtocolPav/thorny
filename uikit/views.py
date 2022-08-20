import discord
from discord.ui import View, Select, Button
from thorny_core.uikit.modals import ProfileEditMain, ProfileEditLore
from thorny_core.uikit.embeds import profile_edit_embed
from thorny_core.uikit.slashoptions import profile_main_select, profile_lore_select, profile_stats_select
from thorny_core.db import User


class ProfileEdit(View):
    def __init__(self, thorny_user: User, embed: discord.Embed):
        super().__init__(timeout=None)
        self.profile_owner = thorny_user
        self.edit_embed = embed

    @discord.ui.select(placeholder="🧑 Main Page | Choose a section to edit",
                       options=profile_main_select)
    async def main_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(ProfileEditMain(select_menu.values[0], self.profile_owner,
                                                              self.edit_embed))

    @discord.ui.select(placeholder="⚔️ Lore Page | Choose a section to edit",
                       options=profile_lore_select)
    async def lore_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(ProfileEditLore(select_menu.values[0], self.profile_owner,
                                                              self.edit_embed))

    @discord.ui.select(placeholder="📊 Stats Page | Choose a section to edit",
                       options=profile_stats_select)
    async def stats_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(ProfileEditLore(select_menu.values[0], self.profile_owner,
                                                              self.edit_embed))


class Profile(View):
    def __init__(self, thorny_user: User, pages: list, ctx: discord.ApplicationContext):
        super().__init__(timeout=30.0)
        self.profile_owner = thorny_user
        self.page = 0
        self.ctx = ctx
        self.pages = pages
        self.main_hint = "Main"
        self.lore_hint = "Lore"
        self.activity_hint = "Stats"

    async def update_buttons(self):
        prev_arrow = [x for x in self.children if x.custom_id == "previous_page_arrow"][0]
        next_arrow = [x for x in self.children if x.custom_id == "next_page_arrow"][0]

        if self.page == 0:
            prev_arrow.label = "<"
            prev_arrow.disabled = True
            next_arrow.label = self.lore_hint + " >"
            next_arrow.disabled = False
        elif self.page == 1:
            prev_arrow.label = "< " + self.main_hint
            prev_arrow.disabled = False
            next_arrow.label = self.activity_hint + " >"
            next_arrow.disabled = False
        elif self.page == 2:
            prev_arrow.label = "< " + self.lore_hint
            prev_arrow.disabled = False
            next_arrow.label = ">"
            next_arrow.disabled = True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.ctx.edit(view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray,
                       label="<",
                       disabled=True,
                       custom_id="previous_page_arrow")
    async def previous_page_callback(self, button: Button, interaction: discord.Interaction):
        self.page -= 1
        await self.update_buttons()
        await interaction.response.edit_message(embed=self.pages[self.page], view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple,
                       label="Edit Profile",
                       custom_id="edit_profile")
    async def edit_profile_callback(self, button: Button, interaction: discord.Interaction):
        if interaction.user == self.profile_owner.discord_member:
            edit_embed = discord.Embed(title="Here's what you edited this session:",
                                       colour=self.profile_owner.discord_member.colour)

            await interaction.response.send_message(embed=await profile_edit_embed(self.profile_owner),
                                                    view=ProfileEdit(self.profile_owner, edit_embed),
                                                    ephemeral=True)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} You can't edit someone elses profile.",
                                                    ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray,
                       label="Lore >",
                       custom_id="next_page_arrow")
    async def next_page_callback(self, button: Button, interaction: discord.Interaction):
        self.page += 1
        await self.update_buttons()
        await interaction.response.edit_message(embed=self.pages[self.page], view=self)
