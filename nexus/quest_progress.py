from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Union
import uuid
import httpx

from nexus import Quest
from nexus.quests.progress_customizations import CustomizationProgress
from nexus.quests.progress_targets import KillTargetProgress, MineTargetProgress, ScriptEventTargetProgress, TargetProgressBase


@dataclass
class ObjectiveProgress:
    progress_id: int
    objective_id: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    target_progress: List[TargetProgressBase]
    customization_progress: CustomizationProgress

    @classmethod
    def _build_target_progress(cls, t_data: dict) -> TargetProgressBase:
        """Factory for specific target progress types"""
        t_type = t_data.get('target_type')
        # Default defaults to 0 if missing
        base_kwargs = {
            'target_uuid': t_data.get('target_uuid', str(uuid.uuid4())),
            'target_type': t_type,
            'count': t_data.get('count', 0)
        }

        if t_type == 'mine':
            return MineTargetProgress(**base_kwargs)
        elif t_type == 'kill':
            return KillTargetProgress(**base_kwargs)
        elif t_type == 'scriptevent':
            return ScriptEventTargetProgress(**base_kwargs)
        else:
            return TargetProgressBase(**base_kwargs)

    @classmethod
    def build(cls, data: dict):
        # 1. Target Progress
        raw_targets = data.get('target_progress', [])
        targets = [cls._build_target_progress(t) for t in raw_targets]

        # 2. Customization Progress
        cust_data = data.get('customization_progress', {})
        cust_progress = CustomizationProgress.build(cust_data)

        # 3. Dates
        start = datetime.fromisoformat(data['start_time']) if data.get('start_time') else None
        end = datetime.fromisoformat(data['end_time']) if data.get('end_time') else None

        return cls(
            progress_id=data['progress_id'],
            objective_id=data['objective_id'],
            start_time=start,
            end_time=end,
            status=data['status'],
            target_progress=targets,
            customization_progress=cust_progress
        )


@dataclass
class QuestProgress:
    progress_id: int
    thorny_id: int
    quest_id: int
    accept_time: datetime
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    objectives: List[ObjectiveProgress]

    @classmethod
    async def build_active(cls, thorny_id: int) -> Optional["QuestProgress"]:
        """Fetches the currently active quest for a user"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://nexuscore:8000/api/v0.2/quests/progress/user/{thorny_id}/active")

            if resp.status_code == 404:
                return None

            data = resp.json()

            # Parse Objectives
            objectives_data = data.pop('objectives', [])
            objectives = [ObjectiveProgress.build(obj) for obj in objectives_data]

            # Parse Dates
            accept = datetime.fromisoformat(data['accept_time'])
            start = datetime.fromisoformat(data['start_time']) if data.get('start_time') else None
            end = datetime.fromisoformat(data['end_time']) if data.get('end_time') else None

            return cls(
                progress_id=data['progress_id'],
                thorny_id=data['thorny_id'],
                quest_id=data['quest_id'],
                accept_time=accept,
                start_time=start,
                end_time=end,
                status=data['status'],
                objectives=objectives
            )

    @classmethod
    async def accept_quest(cls, thorny_id: int, quest_id: int):
        """API call to accept a new quest"""
        async with httpx.AsyncClient() as client:
            await client.post(f"http://nexuscore:8000/api/v0.2/quests/progress/",
                              json={'quest_id': quest_id, 'thorny_id': thorny_id})

    @classmethod
    async def get_available_quests(cls, thorny_id: int) -> list[Quest]:
        async with httpx.AsyncClient() as client:
            # Fetch quests the user has already taken/completed
            unavailable_resp = await client.get(f"http://nexuscore:8000/api/v0.2/quests/progress/user/{thorny_id}")

            # Fetch all currently active quests from the system
            all_quests_resp = await client.get(f"http://nexuscore:8000/api/v0.2/quests?active=true")

            # Handle potential empty/error responses gracefully
            if unavailable_resp.status_code == 200:
                unavailable_quests = unavailable_resp.json()
            else:
                unavailable_quests = []

            if all_quests_resp.status_code == 200:
                quest_list = all_quests_resp.json()
            else:
                quest_list = []

            # Create a set of unavailable quest IDs for O(1) lookup
            # "unavailable_quests" is likely a list of UserQuest/QuestProgress objects
            unavailable_ids = {q['quest_id'] for q in unavailable_quests}

            available_quests = []

            for quest_data in quest_list:
                # Filter out quests the user has already engaged with
                if quest_data['quest_id'] not in unavailable_ids:
                    # Build the Quest object using the existing class method
                    quest_obj = Quest.build_with_data(quest_data)
                    available_quests.append(quest_obj)

            return available_quests

    async def fail(self):
        """API call to manually fail the current quest"""
        async with httpx.AsyncClient() as client:
            await client.delete(f"http://nexuscore:8000/api/v0.2/quests/progress/user/{self.thorny_id}/active")

    def get_objective_progress(self, objective_id: int) -> Optional[ObjectiveProgress]:
        """Helper to find specific objective progress by ID"""
        for obj in self.objectives:
            if obj.objective_id == objective_id:
                return obj
        return None
