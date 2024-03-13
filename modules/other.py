import discord
from discord.ext import commands
from thorny_core import uikit
from thorny_core.db import GuildFactory, UserFactory, ProjectFactory
from datetime import datetime

from thorny_core.db.factory import QuestFactory


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


    @commands.slash_command(description="Configure your server settings")
    @commands.has_permissions(administrator=True)
    async def configure(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=uikit.ServerSetup(),
                          ephemeral=True)

    project = discord.SlashCommandGroup("project", "Project Commands")

    @project.command(description="Apply for a Project!",
                     guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    async def apply(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.user)
        project = await ProjectFactory.create(thorny_user)
        await ctx.respond(view=uikit.ProjectApplicationForm(ctx, thorny_user, project),
                          embed=uikit.project_application_builder_embed(thorny_user, project),
                          ephemeral=True)

    @project.command(description="Use in a Project Thread. View the current project's info",
                     guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    async def view(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.user)
        thorny_guild = await GuildFactory.build(ctx.guild)
        project = await ProjectFactory.fetch_by_thread(ctx.channel_id, thorny_guild)

        await ctx.respond(embed=uikit.project_embed(project))

    @project.command(description="COMING SOON! Give a project progress update",
                     guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    async def progress(self, ctx: discord.ApplicationContext):
        ...

    @project.command(description="COMING SOON! Mark your project as complete",
                     guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    async def complete(self, ctx: discord.ApplicationContext):
        ...

    quests = discord.SlashCommandGroup("quests", "Quest Commands")

    @quests.command(description="View the currently available quests",
                    guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    async def view(self, ctx: discord.ApplicationContext):
        quests = await QuestFactory.fetch_available_quests()

        await ctx.respond(embed=uikit.quests_overview(quests),
                          view=uikit.QuestPanel(ctx))