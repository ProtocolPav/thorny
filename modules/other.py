import discord
from discord.ext import commands
from thorny_core import uikit
from datetime import datetime, timedelta

from thorny_core import nexus, thorny_errors


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

    @project.command(description="Apply for a Project!")
    async def apply(self, ctx: discord.ApplicationContext):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await nexus.ThornyUser.build(ctx.user)
        project = await ProjectFactory.create(thorny_user)
        await ctx.respond(view=uikit.ProjectApplicationForm(ctx, thorny_user, project),
                          embed=uikit.project_application_builder_embed(thorny_user, project),
                          ephemeral=True)

    @project.command(description="Use in a Project Thread. View the current project's info")
    async def view(self, ctx: discord.ApplicationContext):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        thorny_user = await UserFactory.build(ctx.user)
        thorny_guild = await GuildFactory.build(ctx.guild)
        project = await ProjectFactory.fetch_by_thread(ctx.channel_id, thorny_guild)

        await ctx.respond(embed=uikit.project_embed(project))

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
