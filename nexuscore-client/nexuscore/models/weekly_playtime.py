from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WeeklyPlaytime")


@_attrs_define
class WeeklyPlaytime:
    """
    Attributes:
        week (int): The week of the year this data is about
        total (float | None): The total playtime that week in seconds
        unique_players (int): How many unique players played that week
        total_sessions (int): The total amount of sessions that week. (A session is when a user connects and
            disconnects)
        average_playtime_per_session (float | None): The average playtime per session this week in seconds
    """

    week: int
    total: float | None
    unique_players: int
    total_sessions: int
    average_playtime_per_session: float | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        week = self.week

        total: float | None
        total = self.total

        unique_players = self.unique_players

        total_sessions = self.total_sessions

        average_playtime_per_session: float | None
        average_playtime_per_session = self.average_playtime_per_session

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "week": week,
                "total": total,
                "unique_players": unique_players,
                "total_sessions": total_sessions,
                "average_playtime_per_session": average_playtime_per_session,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        week = d.pop("week")

        def _parse_total(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total = _parse_total(d.pop("total"))

        unique_players = d.pop("unique_players")

        total_sessions = d.pop("total_sessions")

        def _parse_average_playtime_per_session(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        average_playtime_per_session = _parse_average_playtime_per_session(d.pop("average_playtime_per_session"))

        weekly_playtime = cls(
            week=week,
            total=total,
            unique_players=unique_players,
            total_sessions=total_sessions,
            average_playtime_per_session=average_playtime_per_session,
        )

        weekly_playtime.additional_properties = d
        return weekly_playtime

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
