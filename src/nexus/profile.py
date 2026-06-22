from dataclasses import dataclass

from nexuscore_client import AuthenticatedClient
from nexuscore_client.models import ProfileUpdate

from src import thorny_errors

import httpx

from nexuscore_client.api.users import partial_update_profile_v1_guilds_me_users_thorny_id_profile_patch


@dataclass
class Profile:
    thorny_id: int
    slogan: str
    aboutme: str
    lore: str
    character_name: str
    character_age: int
    character_race: str
    character_role: str
    character_origin: str
    character_beliefs: str
    agility: int
    valor: int
    strength: int
    charisma: int
    creativity: int
    ingenuity: int

    async def update(self, api: AuthenticatedClient):
        data = {
                  "slogan": self.slogan,
                  "aboutme": self.aboutme,
                  "lore": self.lore,
                  "character_name": self.character_name,
                  "character_age": self.character_age,
                  "character_race": self.character_race,
                  "character_role": self.character_role,
                  "character_origin": self.character_origin,
                  "character_beliefs": self.character_beliefs,
                  "agility": self.agility,
                  "valor": self.valor,
                  "strength": self.strength,
                  "charisma": self.charisma,
                  "creativity": self.creativity,
                  "ingenuity": self.ingenuity
                }

        user = await partial_update_profile_v1_guilds_me_users_thorny_id_profile_patch.asyncio_detailed(
            self.thorny_id,
            client=api,
            body=ProfileUpdate(**data)
        )

        if user.status_code != 200:
            raise thorny_errors.UserUpdateError