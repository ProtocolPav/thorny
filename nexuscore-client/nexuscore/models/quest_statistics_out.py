from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.daily_activity_entry import DailyActivityEntry
    from ..models.objective_statistics import ObjectiveStatistics
    from ..models.quest_completion_bucket import QuestCompletionBucket


T = TypeVar("T", bound="QuestStatisticsOut")


@_attrs_define
class QuestStatisticsOut:
    """
    Attributes:
        quest_id (int): The Quest ID
        title (str): The quest title
        quest_type (str): The quest type
        total_accepts (int): Total number of times this quest has been accepted
        total_pending (int): Players who accepted but never started the quest
        total_started (int): Players who actively began working on objectives
        total_completed (int): Players who completed the quest
        total_failed (int): Players who failed the quest
        completion_rate (float): total_completed / total_accepts. 0 if no accepts.
        started_rate (float): total_started / total_accepts. Indicates whether players bounce before starting.
        unique_players (int): Number of distinct players who accepted the quest
        repeat_attempt_players (int): Number of players who accepted the quest more than once
        objectives (list[ObjectiveStatistics]): Per-objective statistics, sorted by order_index, for funnel/waterfall
            charts
        completion_time_histogram (list[QuestCompletionBucket]): Bucketed completion times for histogram display
        daily_activity (list[DailyActivityEntry]): Daily accepts, completions, and failures for time-series line charts
        avg_completion_time_seconds (int | None | Unset): Average time in seconds to complete the quest
        median_completion_time_seconds (int | None | Unset): Median time in seconds to complete the quest
        fastest_completion_seconds (int | None | Unset): Fastest recorded completion time in seconds
        slowest_completion_seconds (int | None | Unset): Slowest recorded completion time in seconds
    """

    quest_id: int
    title: str
    quest_type: str
    total_accepts: int
    total_pending: int
    total_started: int
    total_completed: int
    total_failed: int
    completion_rate: float
    started_rate: float
    unique_players: int
    repeat_attempt_players: int
    objectives: list[ObjectiveStatistics]
    completion_time_histogram: list[QuestCompletionBucket]
    daily_activity: list[DailyActivityEntry]
    avg_completion_time_seconds: int | None | Unset = UNSET
    median_completion_time_seconds: int | None | Unset = UNSET
    fastest_completion_seconds: int | None | Unset = UNSET
    slowest_completion_seconds: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        quest_id = self.quest_id

        title = self.title

        quest_type = self.quest_type

        total_accepts = self.total_accepts

        total_pending = self.total_pending

        total_started = self.total_started

        total_completed = self.total_completed

        total_failed = self.total_failed

        completion_rate = self.completion_rate

        started_rate = self.started_rate

        unique_players = self.unique_players

        repeat_attempt_players = self.repeat_attempt_players

        objectives = []
        for objectives_item_data in self.objectives:
            objectives_item = objectives_item_data.to_dict()
            objectives.append(objectives_item)

        completion_time_histogram = []
        for completion_time_histogram_item_data in self.completion_time_histogram:
            completion_time_histogram_item = completion_time_histogram_item_data.to_dict()
            completion_time_histogram.append(completion_time_histogram_item)

        daily_activity = []
        for daily_activity_item_data in self.daily_activity:
            daily_activity_item = daily_activity_item_data.to_dict()
            daily_activity.append(daily_activity_item)

        avg_completion_time_seconds: int | None | Unset
        if isinstance(self.avg_completion_time_seconds, Unset):
            avg_completion_time_seconds = UNSET
        else:
            avg_completion_time_seconds = self.avg_completion_time_seconds

        median_completion_time_seconds: int | None | Unset
        if isinstance(self.median_completion_time_seconds, Unset):
            median_completion_time_seconds = UNSET
        else:
            median_completion_time_seconds = self.median_completion_time_seconds

        fastest_completion_seconds: int | None | Unset
        if isinstance(self.fastest_completion_seconds, Unset):
            fastest_completion_seconds = UNSET
        else:
            fastest_completion_seconds = self.fastest_completion_seconds

        slowest_completion_seconds: int | None | Unset
        if isinstance(self.slowest_completion_seconds, Unset):
            slowest_completion_seconds = UNSET
        else:
            slowest_completion_seconds = self.slowest_completion_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "quest_id": quest_id,
                "title": title,
                "quest_type": quest_type,
                "total_accepts": total_accepts,
                "total_pending": total_pending,
                "total_started": total_started,
                "total_completed": total_completed,
                "total_failed": total_failed,
                "completion_rate": completion_rate,
                "started_rate": started_rate,
                "unique_players": unique_players,
                "repeat_attempt_players": repeat_attempt_players,
                "objectives": objectives,
                "completion_time_histogram": completion_time_histogram,
                "daily_activity": daily_activity,
            }
        )
        if avg_completion_time_seconds is not UNSET:
            field_dict["avg_completion_time_seconds"] = avg_completion_time_seconds
        if median_completion_time_seconds is not UNSET:
            field_dict["median_completion_time_seconds"] = median_completion_time_seconds
        if fastest_completion_seconds is not UNSET:
            field_dict["fastest_completion_seconds"] = fastest_completion_seconds
        if slowest_completion_seconds is not UNSET:
            field_dict["slowest_completion_seconds"] = slowest_completion_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_activity_entry import DailyActivityEntry
        from ..models.objective_statistics import ObjectiveStatistics
        from ..models.quest_completion_bucket import QuestCompletionBucket

        d = dict(src_dict)
        quest_id = d.pop("quest_id")

        title = d.pop("title")

        quest_type = d.pop("quest_type")

        total_accepts = d.pop("total_accepts")

        total_pending = d.pop("total_pending")

        total_started = d.pop("total_started")

        total_completed = d.pop("total_completed")

        total_failed = d.pop("total_failed")

        completion_rate = d.pop("completion_rate")

        started_rate = d.pop("started_rate")

        unique_players = d.pop("unique_players")

        repeat_attempt_players = d.pop("repeat_attempt_players")

        objectives = []
        _objectives = d.pop("objectives")
        for objectives_item_data in _objectives:
            objectives_item = ObjectiveStatistics.from_dict(objectives_item_data)

            objectives.append(objectives_item)

        completion_time_histogram = []
        _completion_time_histogram = d.pop("completion_time_histogram")
        for completion_time_histogram_item_data in _completion_time_histogram:
            completion_time_histogram_item = QuestCompletionBucket.from_dict(completion_time_histogram_item_data)

            completion_time_histogram.append(completion_time_histogram_item)

        daily_activity = []
        _daily_activity = d.pop("daily_activity")
        for daily_activity_item_data in _daily_activity:
            daily_activity_item = DailyActivityEntry.from_dict(daily_activity_item_data)

            daily_activity.append(daily_activity_item)

        def _parse_avg_completion_time_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        avg_completion_time_seconds = _parse_avg_completion_time_seconds(d.pop("avg_completion_time_seconds", UNSET))

        def _parse_median_completion_time_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        median_completion_time_seconds = _parse_median_completion_time_seconds(
            d.pop("median_completion_time_seconds", UNSET)
        )

        def _parse_fastest_completion_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        fastest_completion_seconds = _parse_fastest_completion_seconds(d.pop("fastest_completion_seconds", UNSET))

        def _parse_slowest_completion_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        slowest_completion_seconds = _parse_slowest_completion_seconds(d.pop("slowest_completion_seconds", UNSET))

        quest_statistics_out = cls(
            quest_id=quest_id,
            title=title,
            quest_type=quest_type,
            total_accepts=total_accepts,
            total_pending=total_pending,
            total_started=total_started,
            total_completed=total_completed,
            total_failed=total_failed,
            completion_rate=completion_rate,
            started_rate=started_rate,
            unique_players=unique_players,
            repeat_attempt_players=repeat_attempt_players,
            objectives=objectives,
            completion_time_histogram=completion_time_histogram,
            daily_activity=daily_activity,
            avg_completion_time_seconds=avg_completion_time_seconds,
            median_completion_time_seconds=median_completion_time_seconds,
            fastest_completion_seconds=fastest_completion_seconds,
            slowest_completion_seconds=slowest_completion_seconds,
        )

        quest_statistics_out.additional_properties = d
        return quest_statistics_out

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
