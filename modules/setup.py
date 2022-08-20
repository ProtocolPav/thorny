import discord
from discord.ext import commands


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])


class Configurations(commands.Cog):
    def __init__(self, client):
        self.client: discord.Bot = client

    @commands.slash_command(description="Run for first-time setup | Don't use again, as this resets ALL settings")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: discord.ApplicationContext):
        overrides = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                     ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                     ctx.guild.owner: discord.PermissionOverwrite(read_messages=True)}
        channel = await ctx.guild.create_text_channel('thorny-setup', overwrites=overrides, position=0,
                                                      reason="Created channel for Thorny Setup")
        await ctx.respond(f"I've created a channel, {channel.mention}, for the setup process!")

        def check(message):
            return message.author == ctx.author and message.channel == channel

        setup_embed = discord.Embed(colour=ctx.user.colour, title="Welcome To Thorny Setup!")
        setup_embed.add_field(name="Let's get started",
                              value="There's a few things we should set up, these are needed so I can work exactly "
                                    "like you want me to work! Here's an overview of what we will be doing:\n"
                                    "- User channel setup (Where Joins, Leaves and Birthday messages show up)\n"
                                    "- Thorny Levels\n"
                                    "- Thorny Logs channel\n"
                                    "- Timeout role and Timeout Channel (Coming in a future update)\n"
                                    "- Channel for Thorny Update messages")
        await channel.send(embed=setup_embed)
        setup_embed.clear_fields()
        setup_embed.add_field(name="User Events",
                              value="If you'd like me to send messages in a channel when a user Joins, Leaves or "
                                    "has a Birthday, then I'll need the name OR id of that channel.\n"
                                    f"Here's an example: {channel.mention} or {channel.id}\n\n"
                                    "If you do **not** want me to send messages like these, type `No`")
        await channel.send(embed=setup_embed)
        checked = False
        join_channel = None
        while not checked:
            join_channel = await self.client.wait_for('message', check=check)
            if "no" in join_channel.content.lower():
                checked = True
                await channel.send("That's fine. Not everyone wants join messages. But they *are* amazing!")
            elif "<#" not in join_channel.content:
                try:
                    int(join_channel)
                    checked = True
                    await channel.send(f"Great! The user events channel has been set to {join_channel.content}.\n"
                                       f"You can edit the Welcome and Leaving message later using `/settings`")
                except ValueError:
                    await channel.send("This doesn't look like a channel ID...")
            else:
                checked = True
                await channel.send(f"Great! The user events channel has been set to {join_channel.content}")

        setup_embed.clear_fields()
        setup_embed.add_field(name="Leveling Up with Thorny",
                              value="Like some other bots, I have a levels system. Luckily for you, you can "
                                    "customize mine for free unlike those other bots!\n"
                                    "Do you want to enable Leveling? (Yes/No)")
        await channel.send(embed=setup_embed)
        checked = False
        leveling = None
        while not checked:
            leveling = await self.client.wait_for('message', check=check)
            if "no" in leveling.content:
                leveling = "Disabled"
                checked = True
                await channel.send("You chose to disable leveling. You will still be able to see commands, but "
                                   "people will not gain XP from messaging.")
            else:
                leveling = "Enabled"
                checked = True
                await channel.send("You chose to enable leveling! Woo! People will gain XP by messaging and using "
                                   "`/disconnect`. XP can only be gained once per minute, this should stop spam.")

        setup_embed.clear_fields()
        setup_embed.add_field(name="Logging with Thorny",
                              value="I can provide you some very useful logs. Everything ranging from "
                                    "message edits, message deletion, to connections and disconnections. "
                                    "More to come in future updates, and more customization\n"
                                    "Mention or type the ID of the channel you'd like logs in. "
                                    "Otherwise, type 'No'")
        await channel.send(embed=setup_embed)
        checked = False
        log_channel = None
        while not checked:
            log_channel = await self.client.wait_for('message', check=check)
            if "no" in log_channel.content.lower():
                checked = True
                await channel.send("That's okay, just remember that you can enable logs at any time :)")
            elif "<#" not in log_channel.content:
                try:
                    int(log_channel)
                    checked = True
                    await channel.send(f"Great! The user logs channel has been set to {log_channel.content}.\n"
                                       f"You can edit what logs get sent later on by running `/settings`")
                except ValueError:
                    await channel.send("This doesn't look like a channel ID...")
            else:
                checked = True
                await channel.send(f"Great! The user logs channel has been set to {log_channel.content}.\n"
                                   f"You can edit what logs get sent later on by running `/settings`")

        setup_embed.clear_fields()
        setup_embed.add_field(name="Thorny Updates",
                              value="I regularly get updated by my creator, Pav. If you'd like to get messages sent "
                                    "whenever I get updated, along with changelogs, just type in a channel ID or "
                                    "mention it.\n"
                                    "Otherwise, type 'No'")
        await channel.send(embed=setup_embed)
        checked = False
        updates_channel = None
        while not checked:
            while not checked:
                updates_channel = await self.client.wait_for('message', check=check)
                if "no" in updates_channel.content.lower():
                    checked = True
                    await channel.send("That's okay, just remember that you can enable logs at any time :)")
                elif "<#" not in updates_channel.content:
                    try:
                        int(updates_channel)
                        checked = True
                        await channel.send(f"Great! The updates channel has been set to {updates_channel.content}.\n")
                    except ValueError:
                        await channel.send("This doesn't look like a channel ID...")
                else:
                    checked = True
                    await channel.send(f"Great! The updates channel has been set to {updates_channel.content}.\n")

        setup_embed.clear_fields()
        setup_embed.add_field(name="That's it!",
                              value="We are done setting things up now. I have more options that you can configure "
                                    "by using the `/settings` command, coming in a future update.\n"
                                    "As of now, here's what you've configured:\n"
                                    f"**User Events Channel**: {join_channel.content}\n"
                                    f"**Leveling**: {leveling}\n"
                                    f"**Logs Channel**: {log_channel.content}\n"
                                    f"**Updates Channel**: {updates_channel.content}\n\n"
                                    f"You can delete this channel now if you want!")
        await channel.send(embed=setup_embed)

    @commands.slash_command()
    async def modal_test(self, ctx: discord.ApplicationContext):
        modal = MyModal(title="Modal via Slash Command")
        await ctx.send_modal(modal)
