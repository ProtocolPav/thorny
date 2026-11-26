from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.random_count import RandomCount


T = TypeVar("T", bound="MaximumDeathsOption")


@_attrs_define
class MaximumDeathsOption:
    """
    Attributes:
        chance (float): The chance (0 to 1) of this customization being added to the generated quest
        deaths (RandomCount): A randomizable number. Either an inclusive `min`/`max` range, or a list of `choices`.
        fail (bool | Unset): Fail the quest when the death count is exceeded Default: True.
    """

    chance: float
    deaths: RandomCount
    fail: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chance = self.chance

        deaths = self.deaths.to_dict()

        fail = self.fail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chance": chance,
                "deaths": deaths,
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

        deaths = RandomCount.from_dict(d.pop("deaths"))

        fail = d.pop("fail", UNSET)

        maximum_deaths_option = cls(
            chance=chance,
            deaths=deaths,
            fail=fail,
        )

        maximum_deaths_option.additional_properties = d
        return maximum_deaths_option

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
