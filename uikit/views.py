import random

import discord
from discord import Interaction
from discord.ui import Item, View, Select, Button, InputText
from datetime import datetime, timedelta
import thorny_core.uikit.modals as modals
from thorny_core.uikit import embeds, options
from thorny_core import thorny_errors

from thorny_core import nexus


class ProfileEdit(View):
    def __init__(self, thorny_user: nexus.ThornyUser, embed: discord.Embed):
        super().__init__(timeout=None)
        self.profile_owner = thorny_user
        self.edit_embed = embed

    @discord.ui.select(placeholder="🧑 Main Page | Choose a section to edit",
                       options=options.profile_main_select())
    async def main_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.ProfileEditMain(select_menu.values[0], self.profile_owner,
                                                                     self.edit_embed))

    @discord.ui.select(placeholder="⚔️ Lore Page | Choose a section to edit",
                       options=options.profile_lore_select())
    async def lore_menu_callback(self, select_menu: Select, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.ProfileEditLore(select_menu.values[0], self.profile_owner,
                                                                     self.edit_embed))


class Profile(View):
    def __init__(self, thorny_user: nexus.ThornyUser, pages: list, ctx: discord.ApplicationContext):
        super().__init__(timeout=120.0)
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
            raise thorny_errors.WrongUser

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

    @staticmethod
    def check_for_community_manager(interaction: discord.Interaction):
        for role in interaction.user.roles:
            if role.name.lower() == "community manager":
                return True

        return False

    @discord.ui.button(style=discord.ButtonStyle.green,
                       label="Approve",
                       custom_id="approve")
    async def approve_callback(self, button: Button, interaction: discord.Interaction):
        thorny_guild = await nexus.ThornyGuild.build(interaction.guild)
        project = await nexus.Project.build(interaction.message.embeds[0].footer.text)

        if self.check_for_community_manager(interaction):
            self.disable_all_items()
            modal = modals.ProjectApplicationExtraInfo(title="Give A Reason",
                                                       label="Why are you accepting this project?",
                                                       placeholder="eg: Good description, trustworthy, dedicated player")
            await interaction.response.send_modal(modal=modal)
            await modal.wait()

            interaction.message.embeds[0].colour = 0x50C878
            interaction.message.embeds[0].set_field_at(2,
                                                       name="CM Comments:",
                                                       value=f"{interaction.message.embeds[0].fields[2].value}\n"
                                                             f"{interaction.user.mention}: {modal.children[0].value}",
                                                       inline=False)

            interaction.message.embeds[0].set_field_at(3,
                                                       name="**STATUS:**",
                                                       value=f"APPROVED by {interaction.user.mention}",
                                                       inline=False)

            await interaction.followup.edit_message(message_id=interaction.message.id,
                                                    embed=interaction.message.embeds[0],
                                                    view=None)

            forum: discord.ForumChannel = interaction.guild.get_channel(thorny_guild.get_channel_id('project_forum'))
            new_project_tag = None

            for tag in forum.available_tags:
                if tag.name == "New Project":
                    new_project_tag = tag

            thread = await forum.create_thread(name=project.name,
                                               content=project.description,
                                               embed=embeds.project_embed(project),
                                               applied_tags=[new_project_tag])

            project.thread_id = thread.id
            await project.set_status('ongoing')
            await project.update()

            await thread.send(f"<@&1079703011451998208>, A new project has been accepted!")
        else:
            await interaction.response.send_message("You've got to have the Community Manager role to do anything.",
                                                    ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.gray,
                       label="Add Comments",
                       custom_id="enter_extra_info")
    async def info_callback(self, button: Button, interaction: discord.Interaction):
        if self.check_for_community_manager(interaction):
            modal = modals.ProjectApplicationExtraInfo(title="Enter Comments",
                                                       label="Comment on the project",
                                                       placeholder="Anything you'd like them to change, anything you like")
            await interaction.response.send_modal(modal=modal)
            await modal.wait()

            interaction.message.embeds[0].set_field_at(2,
                                                       name="CM Comments:",
                                                       value=f"{interaction.message.embeds[0].fields[2].value}\n"
                                                             f"{interaction.user.mention}: {modal.children[0].value}",
                                                       inline=False)

            await interaction.followup.edit_message(message_id=interaction.message.id,
                                                    embed=interaction.message.embeds[0])
        else:
            await interaction.response.send_message("You've got to have the Community Manager role to do anything.",
                                                    ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.blurple,
                       label="Place On Waiting List",
                       custom_id="waiting_list")
    async def waiting_callback(self, button: Button, interaction: discord.Interaction):
        if self.check_for_community_manager(interaction):
            modal = modals.ProjectApplicationExtraInfo(title="Give A Reason",
                                                       label="Why are you wait-listing this project?",
                                                       placeholder="eg: Large Projects need to be discussed by all CMs before approval")
            await interaction.response.send_modal(modal=modal)
            await modal.wait()

            interaction.message.embeds[0].colour = 0x702963
            interaction.message.embeds[0].set_field_at(2,
                                                       name="CM Comments:",
                                                       value=f"{interaction.message.embeds[0].fields[2].value}\n"
                                                             f"{interaction.user.mention}: {modal.children[0].value}",
                                                       inline=False)

            interaction.message.embeds[0].set_field_at(3,
                                                       name="**STATUS:**",
                                                       value="ON WAITING LIST\n"
                                                             "*Your application has been placed on a waiting list.\n"
                                                             "Don't worry, it'll be approved eventually!*",
                                                       inline=False)

            await interaction.followup.edit_message(message_id=interaction.message.id,
                                                    embed=interaction.message.embeds[0])
        else:
            await interaction.response.send_message("You've got to have the Community Manager role to do anything.",
                                                    ephemeral=True)

    # @discord.ui.button(style=discord.ButtonStyle.red,
    #                    label="Deny",
    #                    custom_id="project_deny")
    # async def project_deny_callback(self, button: Button, interaction: discord.Interaction):
    #     project_id = int(interaction.message.embeds[0].footer.text.split("PR")[1])
    #     thorny_id = int(interaction.message.embeds[0].footer.text.split("PR")[0])
    #
    #     thorny_guild = await GuildFactory.build(interaction.guild)
    #     thorny_user = await UserFactory.fetch_by_id(thorny_guild, thorny_id)
    #     project = await ProjectFactory.build(project_id, thorny_user)
    #
    #     if self.check_for_community_manager(interaction):
    #         modal = modals.ProjectApplicationExtraInfo(title="Give A Reason",
    #                                                    label="Why are you denying this project?",
    #                                                    placeholder="eg: Invalid Coordinates / Do not trust player to complete")
    #         await interaction.response.send_modal(modal=modal)
    #         await modal.wait()
    #
    #         interaction.message.embeds[0].colour = 0xD22B2B
    #         interaction.message.embeds[0].set_field_at(2,
    #                                                    name="CM Comments:",
    #                                                    value=f"{interaction.message.embeds[0].fields[2].value}\n"
    #                                                          f"{interaction.user.mention}: {modal.children[0].value}",
    #                                                    inline=False)
    #
    #         interaction.message.embeds[0].set_field_at(3,
    #                                                    name="**STATUS:**",
    #                                                    value="DENIED",
    #                                                    inline=False)
    #
    #         self.disable_all_items()
    #         await interaction.followup.edit_message(message_id=interaction.message.id,
    #                                                 embed=interaction.message.embeds[0],
    #                                                 view=None)
    #
    #         project.status = "denied"
    #         project.accept_date = datetime.now()
    #         await commit(project)
    #     else:
    #         await interaction.response.send_message("You've got to have the Community Manager role to do anything.",
    #                                                 ephemeral=True)


class ProjectApplicationMembers(View):
    def __init__(self, ctx: discord.ApplicationContext, thorny_user: nexus.ThornyUser, project: ...):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.thorny_user = thorny_user
        self.project = project

    @discord.ui.user_select(placeholder="Select any other Project members",
                            min_values=0)
    async def member_select_callback(self, select_menu: Select, interaction: discord.Interaction):
        for member in select_menu.values:
            member: discord.Member
            self.project.members = f"{self.project.members}{member.mention}, "
        await interaction.response.edit_message(embed=embeds.project_application_builder_embed(self.thorny_user, self.project),
                                                view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray,
                       label="Next",
                       custom_id="form")
    async def form_callback(self, button: Button, interaction: discord.Interaction):
        new_view = ProjectApplicationForm(self.ctx, self.thorny_user, self.project)
        button = new_view.children[0]
        button.label = "Confirm Submission"
        button.style = discord.ButtonStyle.green

        await interaction.response.edit_message(embed=embeds.project_application_builder_embed(self.thorny_user, self.project),
                                                view=new_view)


class ProjectApplicationForm(View):
    def __init__(self, ctx: discord.ApplicationContext, thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.thorny_user = thorny_user
        self.thorny_guild = thorny_guild
        self.project_data = {'owner_id': thorny_user.thorny_id}

        self.step = 0

    async def on_timeout(self):
        self.disable_all_items()
        await self.ctx.edit(view=self)

    async def on_error(
        self, error: thorny_errors.ThornyError, item: Item, interaction: Interaction
    ) -> None:
        await interaction.response.edit_message(view=None, embed=error.return_embed())

    @discord.ui.button(style=discord.ButtonStyle.gray,
                       label="Start [1/4]",
                       custom_id="form")
    async def form_callback(self, button: Button, interaction: discord.Interaction):
        if "1" in button.label:
            modal = modals.ProjectDetailsName(self.thorny_user, self.project_data, view=self)
            await interaction.response.send_modal(modal=modal)
            await modal.wait()


        elif "2" in button.label:
            modal = modals.ProjectDetailsCoordinates(self.thorny_user, self.project_data, view=self)
            await interaction.response.send_modal(modal=modal)
            await modal.wait()

        elif "3/3" in button.label:
            modal = modals.ProjectDetailsDescription(self.thorny_user, self.project_data, view=self)
            await interaction.response.send_modal(modal=modal)
            await modal.wait()

        # elif "4/4" in button.label:
        #     await interaction.response.edit_message(embed=embeds.project_application_builder_embed(self.thorny_user,
        #                                                                                            self.project_data),
        #                                             view=ProjectApplicationMembers(self.ctx, self.thorny_user,
        #                                                                            self.project_data))

        elif "Confirm" in button.label:
            project = await nexus.Project.create_new_project(self.project_data['name'],
                                                             self.project_data['description'],
                                                             self.project_data['coordinates'],
                                                             self.project_data['owner_id'])

            channel = interaction.client.get_channel(self.thorny_guild.get_channel_id('project_applications'))

            await interaction.response.edit_message(content=f"Thanks for submitting your application! You can check the "
                                                            f"progress in {channel.mention}!\n"
                                                            f"Community Managers need to check through and make sure that "
                                                            f"everything is included.",
                                                    embed=None,
                                                    view=None)

            await channel.send(embed=embeds.project_application_embed(project, self.project_data, self.thorny_user),
                               view=PersistentProjectAdminButtons())


class SetupFeature(View):
    def __init__(self, thorny_guild: nexus.ThornyGuild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.select(placeholder="Manage Server Modules",
                       options=...)
    async def callback(self, select_menu: Select, interaction: discord.Interaction):
        thorny_guild = await GuildFactory.build(interaction.guild)

        # When a user clicks on one of the buttons, if the feature is enabled, it will be removed.
        # If it is not enabled, it will be added.
        # Then, the thorny_guild will commit itself to the db, saving the feature changes.
        # TODO: make the Features setup
        ...

    @discord.ui.button(label="Back",
                       custom_id="back",
                       row=2,
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupWelcome(View):
    def __init__(self, thorny_guild: nexus.ThornyGuild):
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
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['welcome'],
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
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['welcome'],
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

    @discord.ui.channel_select(placeholder="Change Channel",
                               min_values=0, max_values=1, row=2)
    async def channel_callback(self, select_menu: Select, interaction: discord.Interaction):
        self.thorny_guild.channels.__setattr__("welcome_channel", int(select_menu.values[0].id))
        await commit(self.thorny_guild)

        await interaction.response.edit_message(embed=embeds.configure_embed(self.thorny_guild)['welcome'],
                                                view=SetupWelcome(self.thorny_guild))

    @discord.ui.button(label="Back",
                       custom_id="back",
                       row=3,
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupLevels(View):
    def __init__(self, thorny_guild: nexus.ThornyGuild):
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
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['levels'],
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
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['levels'],
                                               view=SetupLevels(modal.thorny_guild))

    @discord.ui.button(label="Enable/Disable Leveling",
                       custom_id="toggle_levels",
                       style=discord.ButtonStyle.green)
    async def toggle_callback(self, button: Button, interation: discord.Interaction):
        self.thorny_guild.levels_enabled = not self.thorny_guild.levels_enabled
        await commit(self.thorny_guild)
        await interation.response.edit_message(embed=embeds.configure_embed(self.thorny_guild)['levels'],
                                               view=SetupLevels(self.thorny_guild))

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
    def __init__(self, thorny_guild: nexus.ThornyGuild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Choose Logs Channel",
                       custom_id="edit_channel",
                       style=discord.ButtonStyle.gray)
    async def channel_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Channel (Please enter Channel ID)",
                               custom_id="logs_channel",
                               placeholder=f"Current Channel ID: {self.thorny_guild.channels.get_channel('logs')}")
        modal = modals.ServerChannelEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['logs'],
                                               view=SetupLogs(modal.thorny_guild))

    @discord.ui.button(label="Back",
                       custom_id="back",
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupUpdates(View):
    def __init__(self, thorny_guild: nexus.ThornyGuild):
        super().__init__(timeout=None)
        self.thorny_guild = thorny_guild

    @discord.ui.button(label="Choose Updates Channel",
                       custom_id="edit_channel",
                       style=discord.ButtonStyle.gray)
    async def channel_callback(self, button: Button, interation: discord.Interaction):
        input_text = InputText(label="Edit Channel (Please enter Channel ID)",
                               custom_id="thorny_updates_channel",
                               placeholder=f"Current Channel ID: {self.thorny_guild.channels.get_channel('thorny_updates')}")
        modal = modals.ServerChannelEdit(input_text, self.thorny_guild)
        await interation.response.send_modal(modal)
        await modal.wait()
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['updates'],
                                               view=SetupUpdates(modal.thorny_guild))

    @discord.ui.button(label="Back",
                       custom_id="back",
                       style=discord.ButtonStyle.red)
    async def back_callback(self, button: Button, interation: discord.Interaction):
        await interation.response.edit_message(content=None,
                                               embed=None,
                                               view=ServerSetup())


class SetupGulag(View):
    def __init__(self, thorny_guild: nexus.ThornyGuild):
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
    def __init__(self, thorny_guild: nexus.ThornyGuild):
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
    def __init__(self, thorny_guild: nexus.ThornyGuild):
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
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['currency'],
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
        await interation.edit_original_response(embed=embeds.configure_embed(modal.thorny_guild)['currency'],
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
                       options=options.server_setup())
    async def callback(self, select_menu: Select, interaction: discord.Interaction):
        thorny_guild = await GuildFactory.build(interaction.guild)

        match select_menu.values[0]:
            case "welcome":
                await interaction.response.edit_message(embed=embeds.configure_embed(thorny_guild)['welcome'],
                                                        view=SetupWelcome(thorny_guild))
            case "levels":
                await interaction.response.edit_message(embed=embeds.configure_embed(thorny_guild)['levels'],
                                                        view=SetupLevels(thorny_guild))
            case "logs":
                await interaction.response.edit_message(embed=embeds.configure_embed(thorny_guild)['logs'],
                                                        view=SetupLogs(thorny_guild))
            case "updates":
                await interaction.response.edit_message(embed=embeds.configure_embed(thorny_guild)['updates'],
                                                        view=SetupUpdates(thorny_guild))
            case "gulag":
                await interaction.response.edit_message(embed=embeds.configure_embed(thorny_guild)['gulag'],
                                                        view=SetupGulag(thorny_guild))
            case "responses":
                await interaction.response.edit_message(embed=embeds.configure_embed(thorny_guild)['responses'],
                                                        view=SetupResponses(thorny_guild))
            case "currency":
                await interaction.response.edit_message(embed=embeds.configure_embed(thorny_guild)['currency'],
                                                        view=SetupCurrency(thorny_guild))


class QuestPanel(View):
    def __init__(self, context: discord.ApplicationContext, thorny_guild: nexus.ThornyGuild, thorny_user: nexus.ThornyUser):
        super().__init__(timeout=None)
        self.ctx = context
        self.thorny_guild = thorny_guild
        self.thorny_user = thorny_user
        self.selected_quest_id = 0

    async def on_timeout(self):
        self.disable_all_items()

    async def update_view(self):
        all_quests = await options.available_quests(self.thorny_user.thorny_id)
        if len(all_quests) == 0:
            self.children[0].options = [discord.SelectOption(label='No quests!',
                                                             value='none...')]
            self.disable_all_items()
        else:
            self.children[0].options = await options.available_quests(self.thorny_user.thorny_id)

    async def update_buttons(self):
        accept_button = [x for x in self.children if x.custom_id == "accept"][0]

        if self.selected_quest_id != 0 and self.thorny_user.quest is None:
            accept_button.disabled = False

    @discord.ui.select(placeholder="View more info about a Quest")
    async def select_callback(self, select_menu: Select, interaction: discord.Interaction):
        self.selected_quest_id = int(select_menu.values[0])
        await self.update_buttons()

        await interaction.response.edit_message(view=self,
                                                embed=embeds.view_quest(await nexus.Quest.build(self.selected_quest_id),
                                                                        self.thorny_guild.currency_emoji))

    @discord.ui.button(label="Accept Quest",
                       custom_id="accept",
                       emoji="✨",
                       style=discord.ButtonStyle.blurple,
                       disabled=True)
    async def accept_callback(self, button: Button, interaction: discord.Interaction):
        if interaction.user == self.thorny_user.discord_member:
            if self.thorny_user.quest is None:
                await nexus.UserQuest.accept_quest(self.thorny_user.thorny_id, self.selected_quest_id)
                self.thorny_user.quest = await nexus.UserQuest.build(self.thorny_user.thorny_id)

            quest_info = await nexus.Quest.build(self.thorny_user.quest.quest_id)

            await interaction.response.edit_message(view=CurrentQuestPanel(self.ctx, self.thorny_guild, self.thorny_user,
                                                                           quest_info),
                                                    embed=embeds.quest_progress(quest_info, self.thorny_user,
                                                                                self.thorny_guild.currency_emoji))
        else:
            raise thorny_errors.WrongUser


class CurrentQuestPanel(View):
    def __init__(self, context: discord.ApplicationContext, thorny_guild: nexus.ThornyGuild, thorny_user: nexus.ThornyUser,
                 quest_info: nexus.Quest):
        super().__init__(timeout=None)
        self.ctx = context
        self.thorny_guild = thorny_guild
        self.thorny_user = thorny_user
        self.quest = quest_info

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(label="Admit Defeat",
                       custom_id="drop",
                       style=discord.ButtonStyle.red)
    async def drop_callback(self, button: Button, interaction: discord.Interaction):
        if interaction.user == self.thorny_user.discord_member:
            await interaction.response.edit_message(embed=embeds.quest_fail_warn(self.quest),
                                                    view=FailQuest(self.ctx, self.thorny_guild, self.thorny_user,
                                                                   self.quest))
        else:
            raise thorny_errors.WrongUser


class FailQuest(View):
    def __init__(self, context: discord.ApplicationContext, thorny_guild: nexus.ThornyGuild, thorny_user: nexus.ThornyUser,
                 quest_info: nexus.Quest):
        super().__init__(timeout=None)
        self.ctx = context
        self.thorny_guild = thorny_guild
        self.thorny_user = thorny_user
        self.quest = quest_info

    async def on_timeout(self):
        self.disable_all_items()

    @discord.ui.button(label="Confirm Admit Defeat",
                       custom_id="drop",
                       style=discord.ButtonStyle.red)
    async def drop_callback(self, button: Button, interaction: discord.Interaction):
        if interaction.user == self.thorny_user.discord_member:
            await self.thorny_user.quest.fail()

            await interaction.response.edit_message(view=None,
                                                    embed=None,
                                                    content=f"## You admitted defeat.\n"
                                                            f"Run `/quests view` to try your luck at another quest!!")
        else:
            raise thorny_errors.WrongUser

    @discord.ui.button(label="Maybe not...",
                       custom_id="back",
                       style=discord.ButtonStyle.green)
    async def back_callback(self, button: Button, interaction: discord.Interaction):
        if interaction.user == self.thorny_user.discord_member:
            await interaction.response.edit_message(view=CurrentQuestPanel(self.ctx, self.thorny_guild,
                                                                           self.thorny_user, self.quest),
                                                    embed=embeds.quest_progress(self.quest,
                                                                                self.thorny_user,
                                                                                self.thorny_guild.currency_emoji))
        else:
            raise thorny_errors.WrongUser


class QuestAdminPanel(View):
    def __init__(self, context: discord.ApplicationContext, thorny_guild: nexus.ThornyGuild, thorny_user: nexus.ThornyUser):
        super().__init__(timeout=None)
        self.ctx = context
        self.thorny_guild = thorny_guild
        self.thorny_user = thorny_user
        self.quest_id = 0

    async def on_timeout(self):
        self.disable_all_items()

    async def update_view(self):
        all_quests = await options.all_quests()
        if len(all_quests) == 0:
            self.children[0].options = [discord.SelectOption(label='No quests!',
                                                             value='none...')]
            select_menu = [x for x in self.children if x.custom_id == "select"][0]
            select_menu.disabled = True
        else:
            self.children[0].options = all_quests

    async def update_buttons(self):
        expire_button = [x for x in self.children if x.custom_id == "expire"][0]

        if self.quest_id != 0 and self.thorny_user.quest is None:
            expire_button.disabled = False
        else:
            expire_button.disabled = True

    @discord.ui.select(placeholder="Select a Quest to Expire",
                       custom_id='select')
    async def select_callback(self, select_menu: Select, interaction: discord.Interaction):
        self.quest_id = int(select_menu.values[0])
        await self.update_buttons()

        await interaction.response.edit_message(view=self,
                                                embed=embeds.view_quest(await QuestFactory.build(self.quest_id),
                                                                        self.thorny_guild.currency.emoji))

    @discord.ui.button(label="Create New Quest",
                       custom_id="create",
                       emoji="✨",
                       style=discord.ButtonStyle.blurple,
                       disabled=True)
    async def create_callback(self, button: Button, interaction: discord.Interaction):
        if interaction.user == self.thorny_user.discord_member:
            if self.thorny_user.quest is None and interaction.user.id == self.thorny_user.user_id:
                await QuestFactory.create_new_user_quest(self.quest_id, self.thorny_user.thorny_id)
                self.thorny_user = await UserFactory.build(self.thorny_user.discord_member)

            await interaction.response.edit_message(view=CurrentQuestPanel(self.ctx, self.thorny_guild, self.thorny_user),
                                                    embed=embeds.quest_progress(self.thorny_user.quest,
                                                                                self.thorny_guild.currency.emoji))
        else:
            raise errors.WrongUser

    @discord.ui.button(label="Expire Quest",
                       custom_id="expire",
                       style=discord.ButtonStyle.danger,
                       disabled=True)
    async def expire_callback(self, button: Button, interaction: discord.Interaction):
        await QuestFactory.expire_quest(self.quest_id)
        self.quest_id = 0
        await self.update_view()
        await self.update_buttons()

        await interaction.response.edit_message(view=self,
                                                embed=embeds.quests_admin_overview(await QuestFactory.fetch_all_quests())
                                                )


class HelpDropdown(View):
    def __init__(self, client: discord.Bot, guild_id: int):
        super().__init__(timeout=0)
        self.client = client

        self.commands = {}

        for cog_name in client.cogs:
            self.commands[cog_name] = []

            for command in client.get_cog(cog_name).walk_commands():
                if isinstance(command, discord.SlashCommand) and command.guild_ids and guild_id in command.guild_ids:
                    self.commands[cog_name].append({"command_name": f'</{command.qualified_name}:{command.qualified_id}>',
                                                    "description": command.description})

        self.default = discord.Embed(title="Home | Thorny Help Center",
                                     description="Use the **Select Menu** to see more about commands!",
                                     color=0x65b39b)
        for cog in self.client.cogs:
            easy_view_text = []

            for command in self.commands[cog]:
                easy_view_text.append(command['command_name'])

            if len(easy_view_text) > 3:
                easy_view_text = f"{'**,** '.join(easy_view_text[0:3])}**,** and more"
            elif len(easy_view_text) <= 3:
                easy_view_text = f"{'**,** '.join(easy_view_text)}"

            if easy_view_text != "":
                self.default.add_field(name=f"**{cog} Commands**",
                                       value=f"{easy_view_text}",
                                       inline=False)

    help_options = [
                   discord.SelectOption(label="Home", description="Go to the Thorny Help Center Home", emoji="🏡", default=True),
                   discord.SelectOption(label="Moderation", description="Commands to moderate your server", emoji="🔎"),
                   discord.SelectOption(label="Money", description="Commands to do with money", emoji="💳"),
                   discord.SelectOption(label="Inventory", description="Commands to do with the Inventory and Shop", emoji="🎒"),
                   discord.SelectOption(label="Profile", description="Commands to do with your profile", emoji="📝"),
                   discord.SelectOption(label="Playtime", description="Commands to do with playtime", emoji="⏰"),
                   discord.SelectOption(label="Level", description="Commands to do with levels", emoji="🌟"),
                   discord.SelectOption(label="Leaderboard", description="Leaderboards... Self explanatory", emoji="🥇"),
                   discord.SelectOption(label="Other", description="Other commands, like /configure", emoji="⚙️")
    ]

    @discord.ui.select(placeholder="Click on a category to see its commands",
                       min_values=1, max_values=1, options=help_options)
    async def callback(self, select, interaction: discord.Interaction):
        category = select.values[0]
        for item in select.options:
            if item.label == select.values[0]:
                index = select.options.index(item)
                select.options[index].default = True
            else:
                index = select.options.index(item)
                select.options[index].default = False
        if category == "Home":
            help_embed = self.default
        else:
            help_embed = discord.Embed(title=f"{category} | Thorny Help Center",
                                       description="Click on a command to use it!",
                                       color=0x65b39b)
            text = ''
            category = category.capitalize()
            for command in self.commands[category]:
                text = f"{text}{command['command_name']}\n```{command['description']}```\n"

            help_embed.add_field(name=f"**{category} Commands**",
                                 value=f"{text}")

        await interaction.response.edit_message(embed=help_embed, view=select.view)