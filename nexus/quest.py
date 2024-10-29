import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

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
    objective_count: int
    objective_type: str
    natural_block: bool
    objective_timer: Optional[timedelta]
    required_mainhand: Optional[str]
    required_location: Optional[list]
    location_radius: int
    rewards: Optional[list[Reward]]

    @classmethod
    def build(cls, data: dict, reward_data: list[dict]):
        rewards = [Reward.build(r) for r in reward_data]

        objective_class = cls(**data, rewards=rewards)

        if objective_class.objective_timer:
            objective_class.objective_timer = timedelta(seconds=data['objective_timer'])

        return objective_class

    def get_objective_requirement_string(self) -> str:
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
            hours, remainder = divmod(self.objective_timer.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            extra_requirements.append(f'- Timer: **{hours}h{minutes}m{seconds}s** '
                                      f'(starts when you {self.objective_type} '
                                      f'the first {block_or_mob})')

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
    async def build(cls, quest_id: int):
        async with httpx.AsyncClient() as client:
            quest = await client.get(f"http://nexuscore:8000/api/v0.1/quests/{quest_id}")

            quest_dict = quest.json()

            objectives = []

            for obj in quest_dict['objectives']:
                rewards = []
                for reward in quest_dict['rewards']:
                    if reward['objective_id'] == obj['objective_id']:
                        rewards.append(reward)

                objectives.append(Objective.build(obj, rewards))

            quest_class = cls(**quest_dict['quest'], objectives=objectives)

            quest_class.start_time = datetime.strptime(quest_dict['quest']['start_time'], "%Y-%m-%d %H:%M:%S")

            if quest_class.end_time:
                quest_class.end_time = datetime.strptime(quest_dict['quest']['end_time'], "%Y-%m-%d %H:%M:%S")

            return quest_class


@dataclass
class UserObjective:
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
            quest = await client.get(f"http://nexuscore:8000/api/v0.1/users/{thorny_id}/quest/active")

            if quest.status_code == 404:
                return None

            quest_dict = quest.json()

            objectives = [UserObjective.build(i) for i in quest_dict['objectives']]

            del quest_dict['objectives']

            return cls(**quest_dict, objectives=objectives, thorny_id=thorny_id)

    @classmethod
    async def get_available_quests(cls, thorny_id: int) -> list[Quest]:
        async with httpx.AsyncClient() as client:
            unavailable_quests = await client.get(f"http://nexuscore:8000/api/v0.1/users/{thorny_id}/quest/all")
            quest_list = await client.get(f"http://nexuscore:8000/api/v0.1/quests")

            unavailable_quests = unavailable_quests.json()
            quest_list = quest_list.json()['current']

            available_quests = []

            for quest in quest_list:
                if not unavailable_quests or quest['quest']['quest_id'] not in unavailable_quests:
                    available_quests.append(await Quest.build(quest['quest']['quest_id']))

            return available_quests

    @classmethod
    async def accept_quest(cls, thorny_id: int, quest_id: int):
        async with httpx.AsyncClient() as client:
            await client.post(f"http://nexuscore:8000/api/v0.1/users/{thorny_id}/quest/{quest_id}")

    async def fail(self):
        async with httpx.AsyncClient() as client:
            await client.delete(f"http://nexuscore:8000/api/v0.1/users/{self.thorny_id}/quest/active")