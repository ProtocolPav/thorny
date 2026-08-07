import discord
from discord.ui import DesignerView

import nexus
import thorny_errors
from uikit import CurrentQuestPanel, embeds


def quests_header(money_symbol: str) -> discord.ui.Container:
    return discord.ui.Container(
        discord.ui.TextDisplay(
            content=(
                "# ✨ Everthorn Quests\n"
                "🔥 **Quests** are a fun distraction from the Minecraft grind\n"
                "📅 New quests are released **weekly**\n"
                "⏲️ Each quest is only available for a **limited time**\n"
                f"{money_symbol} Nugs & other **rewards** are up for grabs!"
            )
        )
    )


class QuestPanel(DesignerView):
    """Lets the user browse available quests and accept one."""

    def __init__(self, context: discord.ApplicationContext, thorny_guild: "nexus.ThornyGuild",
                 thorny_user: "nexus.ThornyUser", available_quests: list):
        self.ctx = context
        self.thorny_guild = thorny_guild
        self.thorny_user = thorny_user
        self.available_quests = available_quests
        self.selected_quest_id = 0

        self.select_menu = discord.ui.Select(
            placeholder="View more info about a Quest",
            options=self._build_options(),
            disabled=len(available_quests) == 0,
        )
        self.select_menu.callback = self.select_callback

        self.accept_button = discord.ui.Button(
            label="Accept Quest",
            custom_id="accept",
            emoji="✨",
            style=discord.ButtonStyle.blurple,
            disabled=True,
        )
        self.accept_button.callback = self.accept_callback

        self.info_container = discord.ui.Container(
            discord.ui.TextDisplay(content="### Select a quest above to view details")
        )

        components = [
            quests_header(thorny_guild.currency_emoji),
            self.info_container,
            discord.ui.Container(
                discord.ui.ActionRow(self.select_menu),
                discord.ui.ActionRow(self.accept_button),
            ),
        ]

        super().__init__(*components, timeout=None)

    def _build_options(self):
        if not self.available_quests:
            return [discord.SelectOption(label="No quests!", value="none")]
        return [
            discord.SelectOption(label=q.title, value=str(q.quest_id))
            for q in self.available_quests
        ]

    async def on_timeout(self):
        self.disable_all_items()

    async def select_callback(self, interaction: discord.Interaction):
        if self.select_menu.values[0] == "none":
            return await interaction.response.defer()

        self.selected_quest_id = int(self.select_menu.values[0])
        self.accept_button.disabled = self.thorny_user.quest is not None

        api = await interaction.client.api.get(interaction.guild.id)
        quest = await nexus.Quest.build(api, self.selected_quest_id)

        [self.info_container.remove_item(x) for x in self.info_container.items]

        self.info_container.add_item(
            discord.ui.MediaGallery(
                discord.MediaGalleryItem(url=f"https://everthorn.net/api/image/quest/overview?questId={quest.quest_id}"),
            )
        )

        await interaction.response.edit_message(view=self)

        return None

    async def accept_callback(self, interaction: discord.Interaction):
        if interaction.user != self.thorny_user.discord_member:
            raise thorny_errors.WrongUser

        api = await interaction.client.api.get(interaction.guild.id)

        if self.thorny_user.quest is None:
            await nexus.QuestProgress.accept_quest(api, self.thorny_user.thorny_id, self.selected_quest_id)
            self.thorny_user.quest = await nexus.QuestProgress.build_active(api, self.thorny_user.thorny_id)

        quest_info = await nexus.Quest.build(api, self.thorny_user.quest.quest_id)

        await interaction.response.edit_message(view=CurrentQuestPanel(self.ctx, self.thorny_guild, self.thorny_user,
                                                                       quest_info),
                                                embed=embeds.quest_progress(quest_info, self.thorny_user.quest,
                                                                            self.thorny_guild.currency_emoji))