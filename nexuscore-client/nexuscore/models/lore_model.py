from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LoreModel")


@_attrs_define
class LoreModel:
    """
    Attributes:
        metadata_type (Literal['lore']): The metadata type
        item_lore (list[str]): The item lore Example: ['This item gives +3 knockback', '+4 Damage'].
    """

    metadata_type: Literal["lore"]
    item_lore: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_type = self.metadata_type

        item_lore = self.item_lore

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_type": metadata_type,
                "item_lore": item_lore,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_type = cast(Literal["lore"], d.pop("metadata_type"))
        if metadata_type != "lore":
            raise ValueError(f"metadata_type must match const 'lore', got '{metadata_type}'")

        item_lore = cast(list[str], d.pop("item_lore"))

        lore_model = cls(
            metadata_type=metadata_type,
            item_lore=item_lore,
        )

        lore_model.additional_properties = d
        return lore_model

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
