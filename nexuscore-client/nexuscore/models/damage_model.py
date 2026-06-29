from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DamageModel")


@_attrs_define
class DamageModel:
    """
    Attributes:
        metadata_type (Literal['damage']): The metadata type
        damage_percentage (float): The percentage of durability the item should lose Example: 0.43.
    """

    metadata_type: Literal["damage"]
    damage_percentage: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_type = self.metadata_type

        damage_percentage = self.damage_percentage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_type": metadata_type,
                "damage_percentage": damage_percentage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_type = cast(Literal["damage"], d.pop("metadata_type"))
        if metadata_type != "damage":
            raise ValueError(f"metadata_type must match const 'damage', got '{metadata_type}'")

        damage_percentage = d.pop("damage_percentage")

        damage_model = cls(
            metadata_type=metadata_type,
            damage_percentage=damage_percentage,
        )

        damage_model.additional_properties = d
        return damage_model

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
