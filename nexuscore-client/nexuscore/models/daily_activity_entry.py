from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DailyActivityEntry")


@_attrs_define
class DailyActivityEntry:
    """
    Attributes:
        date (datetime.date): The calendar date
        accepts (int): Number of quest accepts on this date
        completions (int): Number of quest completions on this date
        failures (int): Number of quest failures on this date
    """

    date: datetime.date
    accepts: int
    completions: int
    failures: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        accepts = self.accepts

        completions = self.completions

        failures = self.failures

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "accepts": accepts,
                "completions": completions,
                "failures": failures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))

        accepts = d.pop("accepts")

        completions = d.pop("completions")

        failures = d.pop("failures")

        daily_activity_entry = cls(
            date=date,
            accepts=accepts,
            completions=completions,
            failures=failures,
        )

        daily_activity_entry.additional_properties = d
        return daily_activity_entry

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
