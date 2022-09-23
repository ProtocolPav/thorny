import discord
from discord.ui import View, Select, Button
from datetime import datetime
import thorny_core.uikit.modals as modals
from thorny_core.uikit.embeds import profile_edit_embed, application_info_embed
from thorny_core.uikit.slashoptions import profile_main_select, profile_lore_select, profile_stats_select
from thorny_core.db import User, UserFactory


class ProfileEdit(View):
    def __init__(self, thorny_user: User, embed: discord.Embed):
        super().__init__(timeout=None)
        self.profile_owner = thorny_user
        self.edit_embed = embed

    @discord.ui.select(placeholder="🧑 Main Page | Choose a section to edit",
                       options=profile_main_select)
    async def main_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.ProfileEditMain(select_menu.values[0], self.profile_owner,
                                                                     self.edit_embed))

    @discord.ui.select(placeholder="⚔️ Lore Page | Choose a section to edit",
                       options=profile_lore_select)
    async def lore_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.ProfileEditLore(select_menu.values[0], self.profile_owner,
                                                                     self.edit_embed))

    @discord.ui.select(placeholder="📊 Stats Page | Choose a section to edit",
                       options=profile_stats_select)
    async def stats_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.ProfileEditLore(select_menu.values[0], self.profile_owner,
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
        self.disable_all_items()
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


class PersistentProjectAdminButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.green,
                       label="Approve",
                       custom_id="approve")
    async def approve_callback(self, button: Button, interaction: discord.Interaction):
        role_list = []
        for role in interaction.user.roles:
            role_list.append(role.name)
        if "Community Manager" in role_list:
            interaction.message.embeds[0].colour = 0x50C878
            interaction.message.embeds[0].set_field_at(2,
                                                       name="**STATUS:**",
                                                       value=f"APPROVED by {interaction.user.mention}\n"
                                                             f"on {datetime.now()}",
                                                       inline=False)

            self.disable_all_items()
            await interaction.response.edit_message(view=None,
                                                    embed=interaction.message.embeds[0])
            forum_channel: discord.ForumChannel = interaction.guild.get_channel(1019825292841328681)
            thread = await forum_channel.create_thread(name=interaction.message.embeds[0].title,
                                                       content=interaction.message.embeds[0].title,
                                                       embed=interaction.message.embeds[0])
            await thread.send("<@&668091613687316500> Please give this thread the 'Ongoing Project' tag.")
            await thread.send(f"<@{interaction.message.embeds[0].footer.text}> Congrats on your project being accepted!"
                              f"\nYou can now start sending updates for everyone to see the progress on your "
                              f"amazing project! Good luck, and most importantly, have fun!")
        else:
            await interaction.response.send_message("Hey! You're not a CM...",
                                                    ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray,
                       label="Enter Extra Info",
                       custom_id="enter_extra_info")
    async def info_callback(self, button: Button, interaction: discord.Interaction):
        role_list = []
        for role in interaction.user.roles:
            role_list.append(role.name)
        if "Community Manager" in role_list:
            modal = modals.ProjectApplicationExtraInfo()
            await interaction.response.send_modal(modal=modal)
            await modal.wait()

            interaction.message.embeds[0].set_field_at(1,
                                                       name="Extra Info:",
                                                       value=f"{modal.children[0].value}",
                                                       inline=False)

            await interaction.followup.edit_message(message_id=interaction.message.id,
                                                    embed=interaction.message.embeds[0])
        else:
            await interaction.response.send_message("Hey! You're not a CM...",
                                                    ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.blurple,
                       label="Place On Waiting List",
                       custom_id="waiting_list")
    async def waiting_callback(self, button: Button, interaction: discord.Interaction):
        role_list = []
        for role in interaction.user.roles:
            role_list.append(role.name)
        if "Community Manager" in role_list:
            interaction.message.embeds[0].colour = 0x702963
            interaction.message.embeds[0].set_field_at(2,
                                                       name="**STATUS:**",
                                                       value="ON WAITING LIST\n"
                                                             "*Your application has been placed on a waiting list.\n"
                                                             "Don't worry, it'll be approved eventually!*",
                                                       inline=False)

            await interaction.response.edit_message(embed=interaction.message.embeds[0])
        else:
            await interaction.response.send_message("Hey! You're not a CM...",
                                                    ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.red,
                       label="Deny",
                       custom_id="deny")
    async def deny_callback(self, button: Button, interaction: discord.Interaction):
        role_list = []
        for role in interaction.user.roles:
            role_list.append(role.name)
        if "Community Manager" in role_list:
            interaction.message.embeds[0].colour = 0xD22B2B
            interaction.message.embeds[0].set_field_at(2,
                                                       name="**STATUS:**",
                                                       value="DENIED",
                                                       inline=False)

            self.disable_all_items()
            await interaction.response.edit_message(view=None,
                                                    embed=interaction.message.embeds[0])
        else:
            await interaction.response.send_message("Hey! You're not a CM...",
                                                    ephemeral=True)


class ProjectApplicationForm(View):
    def __init__(self, ctx: discord.ApplicationContext):
        super().__init__(timeout=60.0)
        self.ctx = ctx

    async def on_timeout(self):
        self.disable_all_items()
        await self.ctx.edit(view=self)

    @discord.ui.button(style=discord.ButtonStyle.green,
                       label="Fill In The Form!",
                       custom_id="form")
    async def form_callback(self, button: Button, interaction: discord.Interaction):
        thorny_user = await UserFactory.build(self.ctx.author)
        modal = modals.ProjectApplicationModal()
        await interaction.response.send_modal(modal=modal)
        await modal.wait()
        channel = interaction.client.get_channel(1019959239713771680)
        await channel.send(embed=await application_info_embed(thorny_user, modal.children),
                           view=PersistentProjectAdminButtons())
