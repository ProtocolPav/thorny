import sys
import traceback
from datetime import datetime

import discord

from src import thorny_errors, uikit
from api_client import ManagedAPIClient
from src.thorny_errors import ThornyError


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

    async def on_application_command_error(self, context: discord.ApplicationContext, exception: ThornyError):
        print(f"Ignoring exception in command {context.command}:", file=sys.stderr)
        traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

        command = context.command
        if command and command.has_error_handler():
            return

        cog = context.cog
        if cog and cog.has_error_handler():
            return

        try:
            await context.respond(embed=exception.return_embed(), ephemeral=True)

        except discord.NotFound:
            error = thorny_errors.UnexpectedError2(str(exception.with_traceback(exception.__traceback__)))
            await context.respond(embed=error.return_embed())

        except AttributeError:
            error = thorny_errors.UnexpectedError2(str(exception.with_traceback(exception.__traceback__)))
            await context.respond(embed=error.return_embed())