import discord
from discord.ui import View, Select, Button, InputText
from datetime import datetime
import thorny_core.uikit.modals as modals
from thorny_core.uikit import embeds
from thorny_core.uikit import slashoptions
from thorny_core.db import User, UserFactory, GuildFactory, Guild


class ProfileEdit(View):
    def __init__(self, thorny_user: User, embed: discord.Embed):
        super().__init__(timeout=None)
        self.profile_owner = thorny_user
        self.edit_embed = embed

    @discord.ui.select(placeholder="🧑 Main Page | Choose a section to edit",
                       options=slashoptions.profile_main_select)
    async def main_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.ProfileEditMain(select_menu.values[0], self.profile_owner,
                                                                     self.edit_embed))

    @discord.ui.select(placeholder="⚔️ Lore Page | Choose a section to edit",
                       options=slashoptions.profile_lore_select)
    async def lore_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.ProfileEditLore(select_menu.values[0], self.profile_owner,
                                                                     self.edit_embed))

    @discord.ui.select(placeholder="📊 Stats Page | Choose a section to edit",
                       options=slashoptions.profile_stats_select)
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

            await interaction.response.send_message(embed=await embeds.profile_edit_embed(self.profile_owner),
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
        await channel.send(embed=await embeds.application_info_embed(thorny_user, modal.children),
                           view=PersistentProjectAdminButtons())


class SetupWelcome(View):
    def __init__(self, thorny_guild: Guild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Edit Join Message",
                       custom_id="edit_join",
                       style=discord.ButtonStyle.blurple)
    async def join_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Join Message",
                               custom_id="join_message",
                               placeholder=f"Current Message: {self.thorny_guild.join_message[0:70]}"
                                           f"{'...' if len(self.thorny_guild.join_message) > 70 else ''}",
                               style=discord.InputTextStyle.long)
        modal = modals.ServerEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['welcome'],
                                               view=SetupWelcome(modal.thorny_guild))

    @discord.ui.button(label="Edit Leave Message",
                       custom_id="edit_leave",
                       style=discord.ButtonStyle.blurple)
    async def leave_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Leave Message",
                               custom_id="leave_message",
                               placeholder=f"Current Message: {self.thorny_guild.leave_message[0:70]}"
                                           f"{'...' if len(self.thorny_guild.leave_message) > 70 else ''}",
                               style=discord.InputTextStyle.long)
        modal = modals.ServerEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['welcome'],
                                               view=SetupWelcome(modal.thorny_guild))

    @discord.ui.button(label="Edit Birthday Message",
                       custom_id="edit_birthday",
                       style=discord.ButtonStyle.blurple,
                       disabled=True)
    async def birthday_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Birthday Message",
                               placeholder=f"Current Message: {self.thorny_guild.join_message}",
                               style=discord.InputTextStyle.long)
        await interation.response.send_modal(modals.ServerEdit(input_text, self.thorny_guild))

    @discord.ui.button(label="Change Channel",
                       custom_id="edit_channel",
                       row=2,
                       style=discord.ButtonStyle.gray)
    async def channel_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Channel (Please enter Channel ID)",
                               custom_id="welcome_channel",
                               placeholder=f"Current Channel ID: {self.thorny_guild.channels.welcome_channel}")
        modal = modals.ServerChannelEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['welcome'],
                                               view=SetupWelcome(modal.thorny_guild))

    @discord.ui.button(label="Back",
                       custom_id="back",
                       row=2,
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupLevels(View):
    def __init__(self, thorny_guild: Guild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Edit Level Up Message",
                       custom_id="edit_level",
                       style=discord.ButtonStyle.blurple)
    async def level_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Level Up Message",
                               custom_id="level_message",
                               placeholder=f"Current Message: {self.thorny_guild.level_message[0:70]}"
                                           f"{'...' if len(self.thorny_guild.level_message) > 70 else ''}",
                               style=discord.InputTextStyle.long)
        modal = modals.ServerEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['levels'],
                                               view=SetupLevels(modal.thorny_guild))

    @discord.ui.button(label="Edit XP Multiplier",
                       custom_id="edit_xp",
                       style=discord.ButtonStyle.blurple)
    async def xp_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit XP Multiplier",
                               custom_id="xp_multiplier",
                               placeholder=f"Current Multiplier: x{self.thorny_guild.xp_multiplier}")
        modal = modals.ServerEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['levels'],
                                               view=SetupLevels(modal.thorny_guild))

    @discord.ui.button(label="Enable/Disable Leveling",
                       custom_id="toggle_levels",
                       disabled=True,
                       style=discord.ButtonStyle.green)
    async def toggle_callback(self, button: Button, interation: discord.Interaction):
        ...

    @discord.ui.button(label="Edit XP-Ban Channels",
                       custom_id="edit_xp_ban",
                       row=2,
                       disabled=True,
                       style=discord.ButtonStyle.gray)
    async def ban_callback(self, button: Button, interation: discord.Interaction):
        ...

    @discord.ui.button(label="Back",
                       custom_id="back",
                       row=2,
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupLogs(View):
    def __init__(self, thorny_guild: Guild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Choose Logs Channel",
                       custom_id="edit_channel",
                       style=discord.ButtonStyle.gray)
    async def channel_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Channel (Please enter Channel ID)",
                               custom_id="logs_channel",
                               placeholder=f"Current Channel ID: {self.thorny_guild.channels.logs_channel}")
        modal = modals.ServerChannelEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['logs'],
                                               view=SetupLogs(modal.thorny_guild))

    @discord.ui.button(label="Back",
                       custom_id="back",
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupUpdates(View):
    def __init__(self, thorny_guild: Guild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Choose Updates Channel",
                       custom_id="edit_channel",
                       style=discord.ButtonStyle.gray)
    async def channel_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Channel (Please enter Channel ID)",
                               custom_id="thorny_updates_channel",
                               placeholder=f"Current Channel ID: {self.thorny_guild.channels.thorny_updates_channel}")
        modal = modals.ServerChannelEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['updates'],
                                               view=SetupUpdates(modal.thorny_guild))

    @discord.ui.button(label="Back",
                       custom_id="back",
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupGulag(View):
    def __init__(self, thorny_guild: Guild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Create Gulag Channel & Role",
                       custom_id="create_channel",
                       disabled=True,
                       style=discord.ButtonStyle.green)
    async def channel_callback(self, button: Button, interation: discord.Interaction):
        ...

    @discord.ui.button(label="Back",
                       custom_id="back",
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupResponses(View):
    def __init__(self, thorny_guild: Guild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Edit Exact Responses",
                       custom_id="edit_exact",
                       disabled=True,
                       style=discord.ButtonStyle.blurple)
    async def exact_callback(self, button: Button, interation: discord.Interaction):
        ...

    @discord.ui.button(label="Edit Wildcard Responses",
                       custom_id="edit_wildcard",
                       disabled=True,
                       style=discord.ButtonStyle.blurple)
    async def wildcard_callback(self, button: Button, interation: discord.Interaction):
        ...

    @discord.ui.button(label="Back",
                       custom_id="back",
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupCurrency(View):
    def __init__(self, thorny_guild: Guild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Edit Currency Name",
                       custom_id="edit_name",
                       style=discord.ButtonStyle.blurple)
    async def name_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Currency Name",
                               custom_id="name",
                               placeholder=f"Current Name: {self.thorny_guild.currency.name}")
        modal = modals.ServerCurrencyEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['currency'],
                                               view=SetupCurrency(modal.thorny_guild))

    @discord.ui.button(label="Edit Currency Emoji",
                       custom_id="edit_emoji",
                       style=discord.ButtonStyle.blurple)
    async def emoji_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Currency Emoji",
                               custom_id="emoji",
                               placeholder=f"Current Emoji: {self.thorny_guild.currency.emoji}")
        modal = modals.ServerCurrencyEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_message(embed=embeds.send_configure_embed(modal.thorny_guild)['currency'],
                                               view=SetupCurrency(modal.thorny_guild))

    @discord.ui.button(label="Back",
                       custom_id="back",
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class ServerSetup(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(placeholder="Configure your server settings",
                       options=slashoptions.server_setup)
    async def callback(self, select_menu: Select, interaction: discord.Interaction):
        thorny_guild = await GuildFactory.build(interaction.guild)

        match select_menu.values[0]:
            case "welcome":
                await interaction.response.edit_message(embed=embeds.send_configure_embed(thorny_guild)['welcome'],
                                                        view=SetupWelcome(thorny_guild))
            case "levels":
                await interaction.response.edit_message(embed=embeds.send_configure_embed(thorny_guild)['levels'],
                                                        view=SetupLevels(thorny_guild))
            case "logs":
                await interaction.response.edit_message(embed=embeds.send_configure_embed(thorny_guild)['logs'],
                                                        view=SetupLogs(thorny_guild))
            case "updates":
                await interaction.response.edit_message(embed=embeds.send_configure_embed(thorny_guild)['updates'],
                                                        view=SetupUpdates(thorny_guild))
            case "gulag":
                await interaction.response.edit_message(embed=embeds.send_configure_embed(thorny_guild)['gulag'],
                                                        view=SetupGulag(thorny_guild))
            case "responses":
                await interaction.response.edit_message(embed=embeds.send_configure_embed(thorny_guild)['responses'],
                                                        view=SetupResponses(thorny_guild))
            case "currency":
                await interaction.response.edit_message(embed=embeds.send_configure_embed(thorny_guild)['currency'],
                                                        view=SetupCurrency(thorny_guild))


