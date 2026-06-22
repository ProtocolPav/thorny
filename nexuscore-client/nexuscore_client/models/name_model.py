from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NameModel")


@_attrs_define
class NameModel:
    """
    Attributes:
        metadata_type (Literal['name']): The metadata type
        item_name (str): The item name Example: Super Secret Note.
    """

    metadata_type: Literal["name"]
    item_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_type = self.metadata_type

        item_name = self.item_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_type": metadata_type,
                "item_name": item_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_type = cast(Literal["name"], d.pop("metadata_type"))
        if metadata_type != "name":
            raise ValueError(f"metadata_type must match const 'name', got '{metadata_type}'")

        item_name = d.pop("item_name")

        name_model = cls(
            metadata_type=metadata_type,
            item_name=item_name,
        )

        name_model.additional_properties = d
        return name_model

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
