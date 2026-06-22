from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PotionModel")


@_attrs_define
class PotionModel:
    """
    Attributes:
        metadata_type (Literal['potion']): The metadata type
        potion_effect (str): The potion effect type Example: minecraft:long_speed.
        potion_delivery (str): The potion delivery type Example: Consume.
    """

    metadata_type: Literal["potion"]
    potion_effect: str
    potion_delivery: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_type = self.metadata_type

        potion_effect = self.potion_effect

        potion_delivery = self.potion_delivery

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_type": metadata_type,
                "potion_effect": potion_effect,
                "potion_delivery": potion_delivery,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_type = cast(Literal["potion"], d.pop("metadata_type"))
        if metadata_type != "potion":
            raise ValueError(f"metadata_type must match const 'potion', got '{metadata_type}'")

        potion_effect = d.pop("potion_effect")

        potion_delivery = d.pop("potion_delivery")

        potion_model = cls(
            metadata_type=metadata_type,
            potion_effect=potion_effect,
            potion_delivery=potion_delivery,
        )

        potion_model.additional_properties = d
        return potion_model

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
