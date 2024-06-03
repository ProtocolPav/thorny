import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

import httpx


@dataclass
class Reward:
    reward_id: int
    quest_id: int
    objective_id: Optional[int]
    balance: Optional[int]
    item: Optional[str]
    count: Optional[int]

    @classmethod
    def build(cls, data: dict):
        return cls(**data)

    def get_reward_display(self, money_symbol: str):
        if self.balance:
            return f"{self.balance} {money_symbol}"
        elif self.item:
            item = self.item.split(':')[1].capitalize().replace('_', ' ')
            return f"{self.count} {item}(s)"


@dataclass
class Objective:
    objective_id: int
    quest_id: int
    objective: str
    order: int
    objective_count: int
    objective_type: str
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

        if self.required_mainhand:
            mainhand = self.required_mainhand.split(':')[1].capitalize().replace('_', ' ')
            extra_requirements.append(f'using **{mainhand}** ')
        if self.required_location:
            extra_requirements.append(f'around the coordinates '
                                      f'**{int(self.required_location[0])}, {int(self.required_location[1])}** ')
            extra_requirements.append(f'(radius {self.location_radius}) ')
        if self.objective_timer:
            hours, remainder = divmod(self.objective_timer.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            extra_requirements.append(f'within **{hours}h{minutes}m{seconds}s**')

        return "".join(extra_requirements)


@dataclass
class Quest:
    quest_id: int
    start_time: datetime
    end_time: Optional[datetime]
    timer: timedelta
    title: str
    description: str
    rewards: Optional[list[Reward]]
    objectives: list[Objective]

    @classmethod
    async def build(cls, quest_id: int):
        async with httpx.AsyncClient() as client:
            quest = await client.get(f"http://nexuscore:8000/api/v0.1/quests/{quest_id}")

            quest_dict = quest.json()

            objectives = []

            for obj in quest_dict['objectives']:
                objective_rewards = []
                for reward in quest_dict['rewards']:
                    if reward['objective_id'] == obj['objective_id']:
                        objective_rewards.append(reward)

                objectives.append(Objective.build(obj, objective_rewards))

            rewards = []

            for reward in quest_dict['rewards']:
                if reward['objective_id'] is None:
                    rewards.append(Reward.build(reward))

            quest_class = cls(**quest_dict['quest'], objectives=objectives, rewards=rewards)

            quest_class.start_time = datetime.strptime(quest_dict['quest']['start_time'], "%Y-%m-%d %H:%M:%S.%f")

            if quest_class.end_time:
                quest_class.end_time = datetime.strptime(quest_dict['quest']['end_time'], "%Y-%m-%d %H:%M:%S.%f")

            if quest_class.timer:
                quest_class.timer = timedelta(seconds=quest_dict['quest']['timer'])

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
    objectives_completed: int
    status: str
    objectives: list[UserObjective]

    @classmethod
    async def build(cls, thorny_id: int):
        async with httpx.AsyncClient() as client:
            quest = await client.get(f"http://nexuscore:8000/api/v0.1/users/thorny-id/{thorny_id}/quest/active")

            quest_dict = quest.json()

            if quest_dict['quest'] is None:
                return None
            else:
                objectives = [UserObjective.build(i) for i in quest_dict['objectives']]
                return cls(**quest_dict['quest'], objectives=objectives, thorny_id=thorny_id)

    async def fail(self):
        async with httpx.AsyncClient() as client:
            await client.delete(f"http://nexuscore:8000/api/v0.1/users/thorny-id/{self.thorny_id}/quest/active")