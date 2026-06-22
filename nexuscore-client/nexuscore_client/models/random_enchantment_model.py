from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RandomEnchantmentModel")


@_attrs_define
class RandomEnchantmentModel:
    """
    Attributes:
        metadata_type (Literal['enchantment_random']): The metadata type
        level_min (int): The minimum XP Level to use for the random enchantments Example: 4.
        level_max (int): The maximum XP Level to use for the random enchantments Example: 10.
        treasure (bool): Whether treasure enchantments are allowed to be added Example: True.
    """

    metadata_type: Literal["enchantment_random"]
    level_min: int
    level_max: int
    treasure: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_type = self.metadata_type

        level_min = self.level_min

        level_max = self.level_max

        treasure = self.treasure

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_type": metadata_type,
                "level_min": level_min,
                "level_max": level_max,
                "treasure": treasure,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_type = cast(Literal["enchantment_random"], d.pop("metadata_type"))
        if metadata_type != "enchantment_random":
            raise ValueError(f"metadata_type must match const 'enchantment_random', got '{metadata_type}'")

        level_min = d.pop("level_min")

        level_max = d.pop("level_max")

        treasure = d.pop("treasure")

        random_enchantment_model = cls(
            metadata_type=metadata_type,
            level_min=level_min,
            level_max=level_max,
            treasure=treasure,
        )

        random_enchantment_model.additional_properties = d
        return random_enchantment_model

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
