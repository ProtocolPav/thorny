from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.daily_playtime import DailyPlaytime
    from ..models.monthly_playtime import MonthlyPlaytime


T = TypeVar("T", bound="PlaytimeSummary")


@_attrs_define
class PlaytimeSummary:
    """
    Attributes:
        thorny_id (int): The ThornyID of a user Example: 34.
        total (float): Total playtime in seconds Example: 3600.
        session (datetime.datetime | None): The date and time when the user connected, or `null` Example: 2024-01-01
            01:00:00+00:00.
        daily (list[DailyPlaytime]):
        monthly (list[MonthlyPlaytime]):
    """

    thorny_id: int
    total: float
    session: datetime.datetime | None
    daily: list[DailyPlaytime]
    monthly: list[MonthlyPlaytime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thorny_id = self.thorny_id

        total = self.total

        session: None | str
        if isinstance(self.session, datetime.datetime):
            session = self.session.isoformat()
        else:
            session = self.session

        daily = []
        for componentsschemas_daily_playtime_list_item_data in self.daily:
            componentsschemas_daily_playtime_list_item = componentsschemas_daily_playtime_list_item_data.to_dict()
            daily.append(componentsschemas_daily_playtime_list_item)

        monthly = []
        for componentsschemas_monthly_playtime_list_item_data in self.monthly:
            componentsschemas_monthly_playtime_list_item = componentsschemas_monthly_playtime_list_item_data.to_dict()
            monthly.append(componentsschemas_monthly_playtime_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thorny_id": thorny_id,
                "total": total,
                "session": session,
                "daily": daily,
                "monthly": monthly,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_playtime import DailyPlaytime
        from ..models.monthly_playtime import MonthlyPlaytime

        d = dict(src_dict)
        thorny_id = d.pop("thorny_id")

        total = d.pop("total")

        def _parse_session(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                session_type_0 = datetime.datetime.fromisoformat(data)

                return session_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        session = _parse_session(d.pop("session"))

        daily = []
        _daily = d.pop("daily")
        for componentsschemas_daily_playtime_list_item_data in _daily:
            componentsschemas_daily_playtime_list_item = DailyPlaytime.from_dict(
                componentsschemas_daily_playtime_list_item_data
            )

            daily.append(componentsschemas_daily_playtime_list_item)

        monthly = []
        _monthly = d.pop("monthly")
        for componentsschemas_monthly_playtime_list_item_data in _monthly:
            componentsschemas_monthly_playtime_list_item = MonthlyPlaytime.from_dict(
                componentsschemas_monthly_playtime_list_item_data
            )

            monthly.append(componentsschemas_monthly_playtime_list_item)

        playtime_summary = cls(
            thorny_id=thorny_id,
            total=total,
            session=session,
            daily=daily,
            monthly=monthly,
        )

        playtime_summary.additional_properties = d
        return playtime_summary

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
