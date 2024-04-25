import discord
from discord.ext import commands
from thorny_core import uikit
from thorny_core.db import GuildFactory, UserFactory, ProjectFactory
from datetime import datetime, timedelta

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
        thorny_user = await UserFactory.build(ctx.user)
        display_quests_overview = True

        if thorny_user.quest:
            if thorny_user.quest.quest_fail_check():
                view = uikit.CurrentQuestPanel(ctx, thorny_user.guild, thorny_user)
                await ctx.respond(embed=uikit.quest_progress(thorny_user.quest, thorny_user.guild.currency.emoji),
                                  view=view,
                                  ephemeral=False)
                display_quests_overview = False
            else:
                await QuestFactory.fail_user_quest(thorny_user.quest.id, thorny_user.thorny_id)

        if display_quests_overview:
            quests = await QuestFactory.fetch_available_quests(thorny_user.thorny_id)

            view = uikit.QuestPanel(ctx, thorny_user.guild, thorny_user)
            await view.update_view()
            await ctx.respond(embed=uikit.quests_overview(quests),
                              view=view,
                              ephemeral=False)

    @quests.command(description="CM ONLY | Manage Quests",
                    guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def manage(self, ctx: discord.ApplicationContext):
        thorny_user = await UserFactory.build(ctx.user)

        quests = await QuestFactory.fetch_all_quests()

        view = uikit.QuestAdminPanel(ctx, thorny_user.guild, thorny_user)
        await view.update_view()
        await ctx.respond(embed=uikit.quests_admin_overview(quests),
                          view=view,
                          ephemeral=True)

    @quests.command(description="CM ONLY | Create a new quest",
                    guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    @commands.has_permissions(administrator=True)
    async def create(self, ctx: discord.ApplicationContext,
                     title: discord.Option(str, "Make a cool title for this quest"),
                     description: discord.Option(str, "Give it an interesting description"),
                     objective: discord.Option(str, "Use minecraft IDs!!! Include minecraft: as a prefix"),
                     amount: discord.Option(int, "How much of the objective should people have to complete?"),
                     objective_type: discord.Option(str, "Select a type", choices=['mine', 'kill']),
                     nugs: discord.Option(int, "How many nugs to give as a reward") = None,
                     item: discord.Option(str, "Use minecraft IDs!!! The item to give out as reward") = None,
                     item_amount: discord.Option(int, "The amount of the item to give as a reward") = 1,
                     mainhand: discord.Option(str, "Use minecraft IDs!!! Include minecraft: as a prefix") = None,
                     location: discord.Option(str, "Please write X, Y, Z separated by commas") = None,
                     radius: discord.Option(int, "The radius of the location area") = 100,
                     timer: discord.Option(str, "Write a number with either m or h. e.g: 45m, 5h, 12h") = None):
        if item and 'minecraft:' not in item:
            item = f"minecraft:{item}"
        if mainhand and 'minecraft:' not in mainhand:
            mainhand = f"minecraft:{mainhand}"
        if location:
            splitted = location.split(',')
            position = (int(splitted[0]), int(splitted[2]))
        else:
            position = None
        if timer:
            if 'm' in timer:
                delta = timedelta(minutes=int(timer.split('m')[0]))
            elif 'h' in timer:
                delta = timedelta(hours=int(timer.split('h')[0]))
            else:
                delta = timedelta(hours=12)
        else:
            delta = None

        await QuestFactory.create_new_quest(title, description, objective, amount, objective_type, nugs, item, item_amount,
                                            mainhand, position, radius, delta)

        await ctx.respond("Successfully created the quest. Run /quests view to check it out!",
                          ephemeral=True)

    @commands.slash_command(description="Place a bid in copper blocks",
                            guild_ids=GuildFactory.get_guilds_by_feature('EVERTHORN'))
    async def bid(self, ctx: discord.ApplicationContext,
                  amount: discord.Option(int,
                                         "Enter a bid amount in Copper Blocks."),
                  unit: discord.Option(int,
                                       "Put the number of the unit you are bidding on. Available: 1-8")):
        chennel = ctx.guild.get_channel(1221157464225874071)
        await chennel.send(content=f'**Unit {unit}**\nFrom: {ctx.user.mention} ({ctx.user.name})\nAmount: {amount} Copper Blocks')
        await ctx.respond(content=f'You have placed a bid of {amount} Copper Blocks for **Unit {unit}**!\n'
                                  f'Use bluffing tactics to ensure that you will be the winner for this unit! '
                                  f'Remember, it is storage WARS.\n'
                                  f'## **Storage Wars: The Blind Bid Rules**'
                                  f'- Nobody else knows how much you *actually* bid. So feel free to bluff!\n'
                                  f'- Your most recent bid counts. You can bid higher or less than your previous bids\n'
                                  f'- Make sure you can pay off your bid within 1 week of bidding closing, otherwise '
                                  f'the unit will be sold to the second highest bidder\n'
                                  f'- Bidding ends on <t:1713024000:f>. Bids placed after that will not count\n'
                                  f'- Hint: There are many quests that give out Copper Blocks! Use `/quests view` to accept!\n'
                                  f'*You should probably note down your bids since this message will disappear soon.*',
                          ephemeral=True)