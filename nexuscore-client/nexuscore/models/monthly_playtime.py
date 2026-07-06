from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MonthlyPlaytime")


@_attrs_define
class MonthlyPlaytime:
    """
    Attributes:
        month (datetime.date): Total playtime in seconds Example: 2024-05-01.
        playtime (float): The month's playtime in seconds Example: 332.89.
    """

    month: datetime.date
    playtime: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month = self.month.isoformat()

        playtime = self.playtime

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "month": month,
                "playtime": playtime,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month = datetime.date.fromisoformat(d.pop("month"))

        playtime = d.pop("playtime")

        monthly_playtime = cls(
            month=month,
            playtime=playtime,
        )

        monthly_playtime.additional_properties = d
        return monthly_playtime

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
