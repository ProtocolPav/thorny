from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InteractionStatistic")


@_attrs_define
class InteractionStatistic:
    """
    Attributes:
        reference (str): The interaction reference Example: minecraft:zombie.
        type_ (str): The interaction type Example: kill.
        count (int): The amount of the block mined, entity killed, etc. Example: 24.
    """

    reference: str
    type_: str
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reference = self.reference

        type_ = self.type_

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reference": reference,
                "type": type_,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reference = d.pop("reference")

        type_ = d.pop("type")

        count = d.pop("count")

        interaction_statistic = cls(
            reference=reference,
            type_=type_,
            count=count,
        )

        interaction_statistic.additional_properties = d
        return interaction_statistic

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
