from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ItemModel")


@_attrs_define
class ItemModel:
    """
    Attributes:
        item_id (str): The minecraft ID of the item Example: minecraft:diamond_sword.
        value (float): The initial block value of one of this item Example: 24.5.
        max_uses (int): The maximum uses this item will have before it's value starts going into the negatives Example:
            128.
        depreciation (float): The depreciation of this item Example: 0.32.
        current_uses (int): The current uses of this item Example: 32.
    """

    item_id: str
    value: float
    max_uses: int
    depreciation: float
    current_uses: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        item_id = self.item_id

        value = self.value

        max_uses = self.max_uses

        depreciation = self.depreciation

        current_uses = self.current_uses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "item_id": item_id,
                "value": value,
                "max_uses": max_uses,
                "depreciation": depreciation,
                "current_uses": current_uses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        item_id = d.pop("item_id")

        value = d.pop("value")

        max_uses = d.pop("max_uses")

        depreciation = d.pop("depreciation")

        current_uses = d.pop("current_uses")

        item_model = cls(
            item_id=item_id,
            value=value,
            max_uses=max_uses,
            depreciation=depreciation,
            current_uses=current_uses,
        )

        item_model.additional_properties = d
        return item_model

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
