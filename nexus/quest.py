import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import LiteralString, Optional

import httpx


@dataclass
class Reward:
    reward_id: int
    quest_id: int
    display_name: Optional[str]
    objective_id: Optional[int]
    balance: Optional[int]
    item: Optional[str]
    count: Optional[int]

    @classmethod
    def build(cls, data: dict):
        return cls(**data)

    def get_reward_display(self, money_symbol: str):
        if self.display_name:
            return self.display_name
        elif self.balance:
            return f"{self.balance} {money_symbol}"
        elif self.item:
            item = self.item.split(':')[1].capitalize().replace('_', ' ')
            return f"{self.count} {item}(s)"


@dataclass
class Objective:
    objective_id: int
    quest_id: int
    objective: str
    description: str
    order: int
    display: Optional[str]
    objective_count: int
    objective_type: str
    natural_block: bool
    objective_timer: Optional[float]
    required_mainhand: Optional[str]
    required_location: Optional[list]
    location_radius: int
    rewards: Optional[list[Reward]]

    @classmethod
    async def build(cls, data: dict):
        async with httpx.AsyncClient() as client:
            rewards = await client.get(f"http://nexuscore:8000/api/v0.2/quests/{data['quest_id']}/objectives/{data['objective_id']}/rewards")
            rewards_dict = rewards.json()

            data['rewards'] = [Reward.build(r) for r in rewards_dict]

            objective_class = cls(**data)

            return objective_class

    def get_objective_requirement_string(self) -> LiteralString | None:
        extra_requirements = []
        block_or_mob = self.objective.replace("minecraft:", "").replace('_', ' ').capitalize()

        if self.natural_block and self.objective_type == 'mine':
            extra_requirements.append(f'- The {block_or_mob} '
                                      f'must be **naturally generated**')
        if self.required_mainhand:
            mainhand = self.required_mainhand.split(':')[1].capitalize().replace('_', ' ')
            extra_requirements.append(f'- Must use **{mainhand}**')
        if self.required_location:
            extra_requirements.append(f'- Around the coordinates '
                                      f'**{int(self.required_location[0])}, {int(self.required_location[1])}** '
                                      f'(radius {self.location_radius})')
        if self.objective_timer:
            hours, remainder = divmod(self.objective_timer, 3600)
            minutes, seconds = divmod(remainder, 60)
            extra_requirements.append(f'- Timer: **{math.trunc(hours)}h{math.trunc(minutes)}m{math.trunc(seconds)}s** '
                                      f'(starts immediately!)')

        return "\n".join(extra_requirements) if extra_requirements else None


@dataclass
class Quest:
    quest_id: int
    start_time: datetime
    end_time: Optional[datetime]
    title: str
    description: str
    objectives: list[Objective]

    @classmethod
    def __build_from_data(cls, quest_dict: dict):
        objectives_dict = quest_dict.pop('objectives')

        objectives = []
        for obj in objectives_dict:
            rewards_dict = obj.pop('rewards')
            objectives.append(Objective(**obj, rewards=[Reward(**rew) for rew in rewards_dict]))

        quest_class = cls(**quest_dict, objectives=objectives)

        try:
            quest_class.start_time = datetime.strptime(quest_dict['start_time'], "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            quest_class.start_time = datetime.strptime(quest_dict['start_time'], "%Y-%m-%d %H:%M:%S")

        if quest_class.end_time:
            try:
                quest_class.end_time = datetime.strptime(quest_dict['end_time'], "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                quest_class.end_time = datetime.strptime(quest_dict['end_time'], "%Y-%m-%d %H:%M:%S")

        return quest_class

    @classmethod
    async def build(cls, quest_id: int):
        async with httpx.AsyncClient() as client:
            quest = await client.get(f"http://nexuscore:8000/api/v0.2/quests/{quest_id}")
            quest_dict: dict = quest.json()
            return cls.__build_from_data(quest_dict)

    @classmethod
    def build_with_data(cls, quest_dict: dict):
        return cls.__build_from_data(quest_dict)


@dataclass
class UserObjective:
    thorny_id: int
    quest_id: int
    objective_id: int
    start: datetime
    end: Optional[datetime]
    completion: int
    status: str

    @classmethod
    def build(cls, data: dict):
        return cls(**data)


@dataclass
class UserQuest:
    thorny_id: int
    quest_id: int
    accepted_on: datetime
    started_on: datetime
    status: str
    objectives: list[UserObjective]

    @classmethod
    async def build(cls, thorny_id: int) -> Optional["UserQuest"]:
        async with httpx.AsyncClient() as client:
            quest = await client.get(f"http://nexuscore:8000/api/v0.2/users/{thorny_id}/quest/active")

            if quest.status_code == 404:
                return None

            quest_dict = quest.json()

            objectives = [UserObjective.build(i) for i in quest_dict['objectives']]

            del quest_dict['objectives']

            return cls(**quest_dict, objectives=objectives)

    @classmethod
    async def get_available_quests(cls, thorny_id: int) -> list[Quest]:
        async with httpx.AsyncClient() as client:
            unavailable_quests = await client.get(f"http://nexuscore:8000/api/v0.2/users/{thorny_id}/quest/all")
            quest_list = await client.get(f"http://nexuscore:8000/api/v0.2/quests")

            unavailable_quests = unavailable_quests.json()
            quest_list = quest_list.json()

            available_quests = []
            unavailable_ids = [x['quest_id'] for x in unavailable_quests]

            if not unavailable_ids:
                available_quests = [Quest.build_with_data(quest) for quest in quest_list]
            else:
                for quest in quest_list:
                    if quest['quest_id'] not in unavailable_ids:
                        available_quests.append(Quest.build_with_data(quest))

            return available_quests

    @classmethod
    async def accept_quest(cls, thorny_id: int, quest_id: int):
        async with httpx.AsyncClient() as client:
            await client.post(f"http://nexuscore:8000/api/v0.2/users/{thorny_id}/quest",
                              json={'quest_id': quest_id, 'thorny_id': thorny_id})

    async def fail(self):
        async with httpx.AsyncClient() as client:
            await client.delete(f"http://nexuscore:8000/api/v0.2/users/{self.thorny_id}/quest/active")