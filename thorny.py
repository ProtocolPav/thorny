from abc import ABC

import discord
from datetime import datetime
import json


class ThornyBot(discord.Bot, ABC):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.version = "v2.0-alpha"
        self.presence = discord.Activity(type=discord.ActivityType.custom,
                                         name=f"")

    async def on_ready(self):
        print(f"LOGGING IS NOT SET UP...")
        print(f"[INFO] Thorny is up and running on {self.version}")
        print(f"[INFO] I am in {len(self.guilds)} Guilds, serving up {len(self.application_commands)} Slash Commands")

        await self.change_presence(activity=self.presence)

thorny = ThornyBot()
config = json.load(open('../thorny_data/config.json', 'r+'))
thorny.run(config['token'])