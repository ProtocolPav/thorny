import discord
from discord.ext import commands
from discord.utils import basic_autocomplete

from thorny_core import uikit
from datetime import datetime, timedelta

from thorny_core import nexus, thorny_errors
from thorny_core.uikit import ProjectCommandOptions


class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_started = datetime.now().replace(microsecond=0)

    @commands.slash_command(description="Access the Thorny Help Center")
    async def help(self, ctx: discord.ApplicationContext):
        view = uikit.HelpDropdown(self.client, ctx.guild.id)
        for item in view.help_options:
            if item.label == "Home":
                index = view.help_options.index(item)
                view.help_options[index].default = True
            else:
                index = view.help_options.index(item)
                view.help_options[index].default = False

        await ctx.respond(embed=view.default, view=view)


    @commands.slash_command(description="Get bot stats")
    async def ping(self, ctx):
        await ctx.respond(embed=uikit.ping_embed(self.client, self.bot_started))

    project = discord.SlashCommandGroup("project", "Project Commands")

    @project.command(description="Apply for a Project!")
    async def apply(self, ctx: discord.ApplicationContext):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(ctx.user)
        await ctx.respond(view=uikit.ProjectApplicationForm(ctx, thorny_user, thorny_guild),
                          embed=uikit.project_application_builder_embed(thorny_user, {}),
                          ephemeral=True)

    @project.command(description="View any project's info")
    async def view(self, ctx: discord.ApplicationContext,
                   project: discord.Option(str,
                                           description='Search for a project to view',
                                           autocomplete=basic_autocomplete(ProjectCommandOptions.get_options))):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(ctx.user)
        project_model = await nexus.Project.build(project)

        if project_model.status != 'completed' and thorny_user.thorny_id == project_model.owner_id:
            view = uikit.Project(ctx, thorny_user, thorny_guild, project_model)
        else:
            view = None

        await ctx.respond(embed=uikit.project_embed(project_model),
                          view=view)

    quests = discord.SlashCommandGroup("quests", "Quest Commands")

    @quests.command(description="View the currently available quests")
    async def view(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(ctx.user)
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)

        if thorny_user.quest:
            quest_info = await nexus.Quest.build(thorny_user.quest.quest_id)

            view = uikit.CurrentQuestPanel(ctx, thorny_guild, thorny_user, quest_info)
            await ctx.respond(embed=uikit.quest_progress(quest_info, thorny_user, thorny_guild.currency_emoji),
                              view=view,
                              ephemeral=False)

        else:
            quests = await nexus.UserQuest.get_available_quests(thorny_user.thorny_id)

            view = uikit.QuestPanel(ctx, thorny_guild, thorny_user)
            await view.update_view()
            await ctx.respond(embed=uikit.quests_overview(quests),
                              view=view,
                              ephemeral=False)


    @commands.slash_command(description="Get a link to the world map")
    async def map(self, ctx: discord.ApplicationContext):
        await ctx.respond(content="https://everthorn.fandom.com/wiki/Map:Everthorn")
