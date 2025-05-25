import discord

from dataclasses import dataclass
import thorny_errors

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
    async def build(cls, thorny_id: int):
        async with httpx.AsyncClient() as client:
            profile = await client.get(f"http://nexuscore:8000/api/v0.2/users/{thorny_id}/profile",
                                       timeout=None)

            return cls(**profile.json(), thorny_id=thorny_id)

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

            user = await client.patch(f"http://nexuscore:8000/api/v0.2/users/{self.thorny_id}/profile",
                                      json=data)

            if user.status_code != 200:
                raise thorny_errors.UserUpdateError