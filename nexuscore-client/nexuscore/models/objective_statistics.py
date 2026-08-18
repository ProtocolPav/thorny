from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ObjectiveStatistics")


@_attrs_define
class ObjectiveStatistics:
    """
    Attributes:
        objective_id (int): The objective ID
        order_index (int): The order of the objective, used for funnel sorting
        description (str): The objective description
        players_reached (int): Number of players who started this objective
        players_completed (int): Number of players who completed this objective
        players_failed (int): Number of players who failed this objective
        completion_rate (float): players_completed / players_reached. 0 if none reached.
        drop_rate (float): players_failed / players_reached. 0 if none reached.
        avg_time_seconds (int | None | Unset): Average time in seconds spent on this objective (start_time to end_time),
            across completions
        median_time_seconds (int | None | Unset): Median time in seconds spent on this objective, across completions
    """

    objective_id: int
    order_index: int
    description: str
    players_reached: int
    players_completed: int
    players_failed: int
    completion_rate: float
    drop_rate: float
    avg_time_seconds: int | None | Unset = UNSET
    median_time_seconds: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        objective_id = self.objective_id

        order_index = self.order_index

        description = self.description

        players_reached = self.players_reached

        players_completed = self.players_completed

        players_failed = self.players_failed

        completion_rate = self.completion_rate

        drop_rate = self.drop_rate

        avg_time_seconds: int | None | Unset
        if isinstance(self.avg_time_seconds, Unset):
            avg_time_seconds = UNSET
        else:
            avg_time_seconds = self.avg_time_seconds

        median_time_seconds: int | None | Unset
        if isinstance(self.median_time_seconds, Unset):
            median_time_seconds = UNSET
        else:
            median_time_seconds = self.median_time_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "objective_id": objective_id,
                "order_index": order_index,
                "description": description,
                "players_reached": players_reached,
                "players_completed": players_completed,
                "players_failed": players_failed,
                "completion_rate": completion_rate,
                "drop_rate": drop_rate,
            }
        )
        if avg_time_seconds is not UNSET:
            field_dict["avg_time_seconds"] = avg_time_seconds
        if median_time_seconds is not UNSET:
            field_dict["median_time_seconds"] = median_time_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        objective_id = d.pop("objective_id")

        order_index = d.pop("order_index")

        description = d.pop("description")

        players_reached = d.pop("players_reached")

        players_completed = d.pop("players_completed")

        players_failed = d.pop("players_failed")

        completion_rate = d.pop("completion_rate")

        drop_rate = d.pop("drop_rate")

        def _parse_avg_time_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        avg_time_seconds = _parse_avg_time_seconds(d.pop("avg_time_seconds", UNSET))

        def _parse_median_time_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        median_time_seconds = _parse_median_time_seconds(d.pop("median_time_seconds", UNSET))

        objective_statistics = cls(
            objective_id=objective_id,
            order_index=order_index,
            description=description,
            players_reached=players_reached,
            players_completed=players_completed,
            players_failed=players_failed,
            completion_rate=completion_rate,
            drop_rate=drop_rate,
            avg_time_seconds=avg_time_seconds,
            median_time_seconds=median_time_seconds,
        )

        objective_statistics.additional_properties = d
        return objective_statistics

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
