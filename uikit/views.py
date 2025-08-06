import random

import discord
from discord import Interaction
from discord.ui import Item, View, Select, Button, InputText
from datetime import date
import uikit
import uikit.modals as modals
from uikit import embeds, options
import thorny_errors
import nexus


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

            await thread.starting_message.edit(embed=embeds.project_embed(project))

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
                                                             self.project_data['owner_id'],
                                                             self.project_data['dimension'])

            channel = interaction.client.get_channel(self.thorny_guild.get_channel_id('project_applications'))

            await interaction.response.edit_message(content=f"Thanks for submitting your application! You can check the "
                                                            f"progress in {channel.mention}!\n"
                                                            f"Community Managers need to check through and make sure that "
                                                            f"everything is included.",
                                                    embed=None,
                                                    view=None)

            await channel.send(embed=embeds.project_application_embed(project, self.project_data, self.thorny_user),
                               view=PersistentProjectAdminButtons())


class Project(View):
    def __init__(self, ctx: discord.ApplicationContext, thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild,
                 project: nexus.Project):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.thorny_user = thorny_user
        self.thorny_guild = thorny_guild
        self.project = project

    async def on_timeout(self):
        self.disable_all_items()
        await self.ctx.edit(view=None)
    
    @discord.ui.button(label="Mark as Complete",
                       custom_id='complete',
                       style=discord.ButtonStyle.green)
    async def complete(self, button: Button, interaction: Interaction):
        class ConfirmCompleteView(discord.ui.View):
            def __init__(self, project: nexus.Project, thorny_user: nexus.ThornyUser, thorny_guild: nexus.ThornyGuild):
                super().__init__(timeout=30)
                self.project = project
                self.thorny_user = thorny_user
                self.thorny_guild = thorny_guild

            @discord.ui.button(label="Confirm Completion",
                               custom_id='confirm_complete',
                               style=discord.ButtonStyle.green)
            async def confirm_complete(self, inner_button: Button, inner_interaction: Interaction):
                await self.project.set_status('completed')
                self.project.completed_on = date.today()
                await self.project.update()

                forum = self.thorny_guild.discord_guild.get_channel(self.thorny_guild.get_channel_id('project_forum'))
                thread = forum.get_thread(self.project.thread_id)

                for tag in forum.available_tags:
                    if tag.name == 'Complete':
                        await thread.edit(applied_tags=[tag])
                        await inner_interaction.response.edit_message(embed=embeds.project_embed(self.project),
                                                                      view=None)

        if self.thorny_user.thorny_id == self.project.owner_id:
            await interaction.response.edit_message(embed=embeds.project_complete_warn(),
                                                    view=ConfirmCompleteView(self.project, self.thorny_user, self.thorny_guild))
        else:
            raise thorny_errors.WrongUser
    


class QuestPanel(View):
    def __init__(self, context: discord.ApplicationContext, thorny_guild: nexus.ThornyGuild, thorny_user: nexus.ThornyUser, available_quests: list):
        super().__init__(timeout=None)
        self.ctx = context
        self.thorny_guild = thorny_guild
        self.thorny_user = thorny_user
        self.selected_quest_id = 0
        self.available_quests = available_quests

    async def on_timeout(self):
        self.disable_all_items()

    async def update_view(self):
        if len(self.available_quests) == 0:
            self.children[0].options = [discord.SelectOption(label='No quests!',
                                                             value='none...')]
            self.disable_all_items()
        else:
            self.children[0].options = await options.available_quests(self.available_quests)

    async def update_buttons(self):
        accept_button = [x for x in self.children if x.custom_id == "accept"][0]

        if self.selected_quest_id != 0 and self.thorny_user.quest is None:
            accept_button.disabled = False

    @discord.ui.select(placeholder="View more info about a Quest")
    async def select_callback(self, select_menu: Select, interaction: discord.Interaction):
        self.selected_quest_id = int(select_menu.values[0])
        await self.update_buttons()

        quest = await nexus.Quest.build(self.selected_quest_id)

        creator = self.thorny_guild.discord_guild.get_member(await nexus.ThornyUser.get_discord_id(quest.created_by))

        await interaction.response.edit_message(view=self,
                                                embed=embeds.view_quest(quest,
                                                                        self.thorny_guild.currency_emoji,
                                                                        creator))

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
