import discord

from dataclasses import dataclass
import thorny_core.errors as thorny_errors

import httpx


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


    @classmethod
    def build(cls, profile: dict, thorny_id: int):
        return cls(**profile, thorny_id=thorny_id)

    async def update(self):
        async with httpx.AsyncClient() as client:
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

            user = await client.patch(f"http://nexuscore:8000/v0.1/api/users/thorny-id/{self.thorny_id}/profile",
                                      json=data)

            if user.status_code != 200:
                raise thorny_errors.UserUpdateError