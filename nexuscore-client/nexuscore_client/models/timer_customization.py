from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TimerCustomization")


@_attrs_define
class TimerCustomization:
    """
    Attributes:
        seconds (int): The timer's seconds Example: 540.
        fail (bool): Fail the quest when the timer ends Example: True.
    """

    seconds: int
    fail: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        seconds = self.seconds

        fail = self.fail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seconds": seconds,
                "fail": fail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        seconds = d.pop("seconds")

        fail = d.pop("fail")

        timer_customization = cls(
            seconds=seconds,
            fail=fail,
        )

        timer_customization.additional_properties = d
        return timer_customization

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
