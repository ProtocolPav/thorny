from datetime import datetime

import discord

import uikit
from api_client import ManagedAPIClient


class ThornyBot(discord.Bot):
    api: ManagedAPIClient

    def __init__(self, *args, api: ManagedAPIClient, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = "v2.0.0"
        self.presence = discord.Activity(type=discord.ActivityType.custom,
                                         name=f"Oooh Yeah :sunglasses:")
        self.api = api

    async def on_ready(self):
        print(f"[{datetime.now().replace(microsecond=0)}] [ONLINE] {self.user}")
        print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Running {self.version}")
        print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] I am in {len(self.guilds)} Guilds")

        self.add_view(uikit.PersistentProjectAdminButtons())

        await self.change_presence(activity=self.presence)

        await self.api.get()