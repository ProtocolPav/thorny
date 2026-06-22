from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EnchantmentModel")


@_attrs_define
class EnchantmentModel:
    """
    Attributes:
        metadata_type (Literal['enchantment']): The metadata type
        enchantment_id (str): The enchantment ID Example: minecraft:sharpness.
        enchantment_level (int): The enchantment level Example: 4.
    """

    metadata_type: Literal["enchantment"]
    enchantment_id: str
    enchantment_level: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_type = self.metadata_type

        enchantment_id = self.enchantment_id

        enchantment_level = self.enchantment_level

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_type": metadata_type,
                "enchantment_id": enchantment_id,
                "enchantment_level": enchantment_level,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_type = cast(Literal["enchantment"], d.pop("metadata_type"))
        if metadata_type != "enchantment":
            raise ValueError(f"metadata_type must match const 'enchantment', got '{metadata_type}'")

        enchantment_id = d.pop("enchantment_id")

        enchantment_level = d.pop("enchantment_level")

        enchantment_model = cls(
            metadata_type=metadata_type,
            enchantment_id=enchantment_id,
            enchantment_level=enchantment_level,
        )

        enchantment_model.additional_properties = d
        return enchantment_model

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
