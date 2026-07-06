from dataclasses import dataclass

from nexuscore import AuthenticatedClient
from nexuscore.api.users import get_user_interactions_v_1_guilds_me_users_thorny_id_interactions_get


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
    async def build(cls, api: AuthenticatedClient, thorny_id: int):
        interactions = await get_user_interactions_v_1_guilds_me_users_thorny_id_interactions_get.asyncio_detailed(thorny_id, client=api)

        if interactions.status_code != 200:
            return cls(blocks_mined=[],
                       blocks_placed=[],
                       kills=[],
                       deaths=[],
                       totals={'mine': 0, 'kill': 0, 'place': 0, 'die': 0, 'use': 0})

        interaction_dict = interactions.parsed.to_dict()

        placed = [Interaction.build(i) for i in interaction_dict['blocks_placed']]
        mined = [Interaction.build(i) for i in interaction_dict['blocks_mined']]
        kills = [Interaction.build(i) for i in interaction_dict['kills']]
        deaths = [Interaction.build(i) for i in interaction_dict['deaths']]

        return cls(blocks_mined=mined,
                   blocks_placed=placed,
                   kills=kills,
                   deaths=deaths,
                   totals=interaction_dict['totals'])