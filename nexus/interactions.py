import random

import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

import httpx


@dataclass
class Interaction:
    reference: str
    type: str
    count: int

    @classmethod
    def build(cls, data: dict):
        return cls(reference=data['reference'].replace('_', ' ').replace('minecraft:', '').capitalize(),
                   type=data['type'],
                   count=data['count'])


@dataclass
class Interactions:
    blocks_placed: list[Interaction]
    blocks_mined: list[Interaction]
    kills: list[Interaction]
    deaths: list[Interaction]
    totals: dict

    @classmethod
    async def build(cls, thorny_id: int):
        async with httpx.AsyncClient() as client:
            interactions = await client.get(f"http://nexuscore:8000/api/v0.1/users/thorny-id/{thorny_id}/interactions",
                                            timeout=None)

            interaction_dict = interactions.json()

            placed = [Interaction.build(i) for i in interaction_dict['blocks_placed']]
            mined = [Interaction.build(i) for i in interaction_dict['blocks_mined']]
            kills = [Interaction.build(i) for i in interaction_dict['kills']]
            deaths = [Interaction.build(i) for i in interaction_dict['deaths']]

            return cls(blocks_mined=mined, blocks_placed=placed, kills=kills, deaths=deaths,
                       totals=interaction_dict['totals'])