import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import LiteralString, Optional, Union

import httpx

from nexus.quests.objective_customizations import Customizations
from nexus.quests.objective_targets import KillTarget, MineTarget, ScriptEventTarget, TargetBase


@dataclass
class Reward:
    reward_id: int
    quest_id: int
    objective_id: int
    display_name: Optional[str]
    balance: Optional[int]
    item: Optional[str]
    count: Optional[int]
    item_metadata: list = field(default_factory=list)

    @classmethod
    def build(cls, data: dict):
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def get_reward_display(self, money_symbol: str):
        if self.display_name:
            return self.display_name
        elif self.balance:
            return f"{self.balance} {money_symbol}"
        elif self.item:
            item = self.item.split(':')[1].capitalize().replace('_', ' ') if ':' in self.item else self.item
            return f"{self.count} {item}(s)"
        return "Unknown Reward"


@dataclass
class Objective:
    objective_id: int
    quest_id: int
    description: str
    display: Optional[str]
    order_index: int
    objective_type: str
    logic: str
    target_count: Optional[int]
    targets: list[TargetBase]
    customizations: Customizations
    rewards: list[Reward] = field(default_factory=list)

    @classmethod
    def build_target(cls, t_data: dict) -> TargetBase:
        """Factory method to create the correct Target subclass"""
        t_type = t_data.get('target_type')
        # Ensure UUID is string
        if 'target_uuid' not in t_data:
            t_data['target_uuid'] = str(uuid.uuid4())

        if t_type == 'mine':
            return MineTarget(
                **{k: v for k, v in t_data.items() if k in MineTarget.__annotations__ or k in TargetBase.__annotations__})
        elif t_type == 'kill':
            return KillTarget(
                **{k: v for k, v in t_data.items() if k in KillTarget.__annotations__ or k in TargetBase.__annotations__})
        elif t_type == 'scriptevent':
            return ScriptEventTarget(
                **{k: v for k, v in t_data.items() if k in ScriptEventTarget.__annotations__ or k in TargetBase.__annotations__})
        else:
            # Fallback for unknown types
            return TargetBase(**{k: v for k, v in t_data.items() if k in TargetBase.__annotations__})

    @classmethod
    async def build(cls, data: dict):
        async with httpx.AsyncClient() as client:
            rewards_resp = await client.get(
                f"http://nexuscore:8000/api/v0.2/quests/{data['quest_id']}/objectives/{data['objective_id']}/rewards"
            )
            rewards = [Reward.build(r) for r in rewards_resp.json()]

            # Build Customizations using the new nested builder
            cust_data = data.get('customizations', {})
            customizations = Customizations.build(cust_data)

            raw_targets = data.get('targets', [])
            targets = [cls.build_target(t) for t in raw_targets]

            valid_keys = cls.__annotations__.keys()
            filtered_data = {k: v for k, v in data.items() if k in valid_keys}

            filtered_data['rewards'] = rewards
            filtered_data['customizations'] = customizations
            filtered_data['targets'] = targets

            return cls(**filtered_data)

    def get_objective_requirement_string(self) -> Optional[str]:
        reqs = []
        cust = self.customizations

        # 1. Natural Block
        if cust.natural_block and self.objective_type == 'mine':
            reqs.append(f'- The blocks must be **naturally generated**')

        # 2. Mainhand
        if cust.mainhand:
            item_name = cust.mainhand.item.split(':')[1].replace('_',
                                                                 ' ').title() if ':' in cust.mainhand.item else cust.mainhand.item
            reqs.append(f'- With **{item_name}**')

        # 3. Location
        if cust.location:
            x, y, z = cust.location.coordinates
            reqs.append(f'- Near **{x}, {y}, {z}** '
                        f'(Radius: {cust.location.horizontal_radius})')

        # 4. Timer
        if cust.timer:
            minutes, seconds = divmod(cust.timer.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            time_str = f"{hours}h {minutes}m {seconds}s".replace("0h ", "").replace(" 0m", "")
            reqs.append(f'- Time Limit: **{time_str}**')

        # 5. Deaths
        if cust.maximum_deaths:
            reqs.append(f'- Max Deaths: **{cust.maximum_deaths.deaths}**')

        # 6. Failure Conditions
        fail_reasons = []
        if cust.timer and cust.timer.fail:
            fail_reasons.append("time runs out")
        if cust.maximum_deaths and cust.maximum_deaths.fail:
            fail_reasons.append("death limit reached")

        if fail_reasons:
            reasons_str = " or ".join(fail_reasons)
            reqs.append(f'- *Failing this objective ({reasons_str}) will fail the entire quest*')

        return "\n".join(reqs) if reqs else None


@dataclass
class Quest:
    quest_id: int
    start_time: datetime
    end_time: Optional[datetime]
    title: str
    description: str
    objectives: list[Objective]
    tags: list[str]
    created_by: int
    quest_type: str

    @classmethod
    def __build_from_data(cls, quest_dict: dict):
        objectives_data = quest_dict.pop('objectives', [])
        objectives = []

        for obj_data in objectives_data:
            # 1. Rewards
            rewards_list = [Reward.build(r) for r in obj_data.pop('rewards', [])]

            # 2. Customizations
            cust_data = obj_data.pop('customizations', {})
            customizations = Customizations.build(cust_data)

            # 3. Targets
            targets_list = [Objective.build_target(t) for t in obj_data.pop('targets', [])]

            # 4. Create Objective
            valid_keys = Objective.__annotations__.keys()
            filtered_obj = {k: v for k, v in obj_data.items() if k in valid_keys}

            objectives.append(Objective(
                **filtered_obj,
                rewards=rewards_list,
                customizations=customizations,
                targets=targets_list
            ))

        if isinstance(quest_dict.get('start_time'), str):
            quest_dict['start_time'] = datetime.fromisoformat(quest_dict['start_time'])
        if isinstance(quest_dict.get('end_time'), str):
            quest_dict['end_time'] = datetime.fromisoformat(quest_dict['end_time'])

        return cls(**quest_dict, objectives=objectives)

    @classmethod
    async def build(cls, quest_id: int):
        async with httpx.AsyncClient() as client:
            quest = await client.get(f"http://nexuscore:8000/api/v0.2/quests/{quest_id}")
            quest_dict: dict = quest.json()
            return cls.__build_from_data(quest_dict)

    @classmethod
    def build_with_data(cls, quest_dict: dict):
        return cls.__build_from_data(quest_dict)

    def get_reward_string(self, money_symbol: str):
        nug_rewards = 0
        item_rewards = 0

        for objective in self.objectives:
            for reward in objective.rewards:
                if reward.balance:
                    nug_rewards += reward.balance
                else:
                    item_rewards += 1

        texts = []
        if nug_rewards:
            texts.append(f"{nug_rewards} {money_symbol}")
        if item_rewards:
            texts.append(f"*+{item_rewards} Item Rewards*")

        return ', '.join(texts)