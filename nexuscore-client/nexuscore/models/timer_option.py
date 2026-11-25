from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.random_count import RandomCount


T = TypeVar("T", bound="TimerOption")


@_attrs_define
class TimerOption:
    """
    Attributes:
        chance (float): The chance (0 to 1) of this customization being added to the generated quest
        seconds (RandomCount): A randomizable number. Either an inclusive `min`/`max` range, or a list of `choices`.
        fail (bool | Unset): Fail the quest when the timer ends Default: True.
    """

    chance: float
    seconds: RandomCount
    fail: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chance = self.chance

        seconds = self.seconds.to_dict()

        fail = self.fail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chance": chance,
                "seconds": seconds,
            }
        )
        if fail is not UNSET:
            field_dict["fail"] = fail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.random_count import RandomCount

        d = dict(src_dict)
        chance = d.pop("chance")

        seconds = RandomCount.from_dict(d.pop("seconds"))

        fail = d.pop("fail", UNSET)

        timer_option = cls(
            chance=chance,
            seconds=seconds,
            fail=fail,
        )

        timer_option.additional_properties = d
        return timer_option

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
