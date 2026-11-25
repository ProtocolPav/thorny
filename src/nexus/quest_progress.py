from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Optional, List
import uuid

from nexuscore import AuthenticatedClient
from nexuscore.models import QuestProgressIn
from src.nexus.quest import DAILY_QUEST_TYPE, Quest
from src.nexus.quests.progress_customizations import CustomizationProgress
from src.nexus.quests.progress_targets import KillTargetProgress, MineTargetProgress, ScriptEventTargetProgress, VisitTargetProgress, TargetProgressBase

from nexuscore.api.quests import (
    get_active_quest_progress_v1_guilds_me_quests_progress_user_thorny_id_active_get,
    create_quest_progress_v1_guilds_me_quests_progress_post,
    list_quest_progress_v1_guilds_me_quests_progress_user_thorny_id_get,
    list_quests_v1_guilds_me_quests_get,
    abandon_active_quest_progress_v1_guilds_me_quests_progress_user_thorny_id_active_delete
)


@dataclass
class ObjectiveProgress:
    progress_id: int
    objective_id: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    target_progress: List[TargetProgressBase]
    customization_progress: CustomizationProgress

    @property
    def current_completion_count(self) -> int:
        """Sums up the count of all targets in this objective progress."""
        return sum(t.count for t in self.target_progress)

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
        elif t_type == 'visit':
            return VisitTargetProgress(**base_kwargs)
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
    async def build_active(cls, api: AuthenticatedClient, thorny_id: int) -> Optional["QuestProgress"]:
        """Fetches the currently active quest for a user"""
        resp = await get_active_quest_progress_v1_guilds_me_quests_progress_user_thorny_id_active_get.asyncio_detailed(thorny_id, client=api)

        if resp.status_code == 404:
            return None

        data = resp.parsed.to_dict()

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
    async def accept_quest(cls, api: AuthenticatedClient, thorny_id: int, quest_id: int):
        """API call to accept a new quest"""
        await create_quest_progress_v1_guilds_me_quests_progress_post.asyncio_detailed(
            client=api,
            body=QuestProgressIn(thorny_id=thorny_id, quest_id=quest_id)
        )

    @classmethod
    async def get_available_quests(cls, api: AuthenticatedClient, thorny_id: int) -> list[Quest]:
        # Fetch quests the user has already taken/completed
        unavailable_resp = await list_quest_progress_v1_guilds_me_quests_progress_user_thorny_id_get.asyncio_detailed(thorny_id, client=api)

        # Fetch all currently active quests from the system.
        # Daily quests are excluded: they are auto-accepted and shown by /quests daily instead
        all_quests_resp = await list_quests_v1_guilds_me_quests_get.asyncio_detailed(
            client=api, active=True, exclude_quest_types=[DAILY_QUEST_TYPE]
        )

        # Handle potential empty/error responses gracefully
        if unavailable_resp.status_code == 200:
            unavailable_quests = [q.to_dict() for q in unavailable_resp.parsed]
        else:
            unavailable_quests = []

        if all_quests_resp.status_code == 200:
            quest_list = [q.to_dict() for q in all_quests_resp.parsed]
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

    @classmethod
    async def get_recently_expired_quest(cls, api: AuthenticatedClient, thorny_id: int,
                                         within_days: int = 7) -> Optional[Quest]:
        """
        Returns the user's most recent regular (non-daily) quest if it expired before they
        finished it, within the last `within_days` days. Nexuscore abandons expired quests
        automatically, so this is how Thorny can still tell the player their quest expired.
        """
        progress_resp = await list_quest_progress_v1_guilds_me_quests_progress_user_thorny_id_get.asyncio_detailed(thorny_id, client=api)
        if progress_resp.status_code != 200 or not progress_resp.parsed:
            return None

        # Recent regular quests, newest first; daily quests expire every day so they're skipped
        quests_resp = await list_quests_v1_guilds_me_quests_get.asyncio_detailed(
            client=api, exclude_quest_types=[DAILY_QUEST_TYPE], page_size=50
        )
        if quests_resp.status_code != 200:
            return None

        regular_quests = {q['quest_id']: q for q in (q.to_dict() for q in quests_resp.parsed)}

        progress = [p.to_dict() for p in progress_resp.parsed]
        latest = max((p for p in progress if p['quest_id'] in regular_quests),
                     key=lambda p: p['accept_time'], default=None)

        if not latest or latest['status'] != 'abandoned' or not latest.get('end_time'):
            return None

        quest = Quest.build_with_data(regular_quests[latest['quest_id']])
        abandoned_at = datetime.fromisoformat(latest['end_time'])

        # Abandoned at or after the quest ended means it expired, rather than being dropped
        expired = quest.end_time is not None and abandoned_at >= quest.end_time
        recent = datetime.now(UTC) - quest.end_time <= timedelta(days=within_days) if expired else False

        return quest if expired and recent else None

    async def abandon(self, api: AuthenticatedClient):
        """API call to abandon (drop) the current quest"""
        await abandon_active_quest_progress_v1_guilds_me_quests_progress_user_thorny_id_active_delete.asyncio_detailed(self.thorny_id, client=api)

    def get_objective_progress(self, objective_id: int) -> Optional[ObjectiveProgress]:
        """Helper to find specific objective progress by ID"""
        for obj in self.objectives:
            if obj.objective_id == objective_id:
                return obj
        return None
