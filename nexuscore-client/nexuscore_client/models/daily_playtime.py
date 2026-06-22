import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="DailyPlaytime")


@_attrs_define
class DailyPlaytime:
    """
    Attributes:
        day (datetime.date): The day this data is about
        total (Union[None, float]): The total playtime that day in seconds
        unique_players (int): How many unique players played that day
        total_sessions (int): The total amount of sessions that day. (A session is when a user connects and disconnects)
        average_playtime_per_session (Union[None, float]): The average playtime per session today in seconds
    """

    day: datetime.date
    total: Union[None, float]
    unique_players: int
    total_sessions: int
    average_playtime_per_session: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        day = self.day.isoformat()

        total: Union[None, float]
        total = self.total

        unique_players = self.unique_players

        total_sessions = self.total_sessions

        average_playtime_per_session: Union[None, float]
        average_playtime_per_session = self.average_playtime_per_session

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "day": day,
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
        day = isoparse(d.pop("day")).date()

        def _parse_total(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        total = _parse_total(d.pop("total"))

        unique_players = d.pop("unique_players")

        total_sessions = d.pop("total_sessions")

        def _parse_average_playtime_per_session(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        average_playtime_per_session = _parse_average_playtime_per_session(d.pop("average_playtime_per_session"))

        daily_playtime = cls(
            day=day,
            total=total,
            unique_players=unique_players,
            total_sessions=total_sessions,
            average_playtime_per_session=average_playtime_per_session,
        )

        daily_playtime.additional_properties = d
        return daily_playtime

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
