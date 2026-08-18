from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_out import UserOut


T = TypeVar("T", bound="SessionOut")


@_attrs_define
class SessionOut:
    """
    Attributes:
        start (datetime.datetime): The time the user connected
        end (datetime.datetime | None):
        duration (float | None):
        user (UserOut):
    """

    start: datetime.datetime
    end: datetime.datetime | None
    duration: float | None
    user: UserOut
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start = self.start.isoformat()

        end: None | str
        if isinstance(self.end, datetime.datetime):
            end = self.end.isoformat()
        else:
            end = self.end

        duration: float | None
        duration = self.duration

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start": start,
                "end": end,
                "duration": duration,
                "user": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_out import UserOut

        d = dict(src_dict)
        start = datetime.datetime.fromisoformat(d.pop("start"))

        def _parse_end(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_type_0 = datetime.datetime.fromisoformat(data)

                return end_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        end = _parse_end(d.pop("end"))

        def _parse_duration(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        duration = _parse_duration(d.pop("duration"))

        user = UserOut.from_dict(d.pop("user"))

        session_out = cls(
            start=start,
            end=end,
            duration=duration,
            user=user,
        )

        session_out.additional_properties = d
        return session_out

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
