from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PinIn")


@_attrs_define
class PinIn:
    """
    Attributes:
        name (str): The name of the pin
        description (str): A short description of the pin, such as what the shop sells, etc.
        coordinates (list[int]): The coordinates of the pin
        dimension (str): The dimension of the pin
        pin_type (str): The type of pin this is
    """

    name: str
    description: str
    coordinates: list[int]
    dimension: str
    pin_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        coordinates = self.coordinates

        dimension = self.dimension

        pin_type = self.pin_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "coordinates": coordinates,
                "dimension": dimension,
                "pin_type": pin_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        coordinates = cast(list[int], d.pop("coordinates"))

        dimension = d.pop("dimension")

        pin_type = d.pop("pin_type")

        pin_in = cls(
            name=name,
            description=description,
            coordinates=coordinates,
            dimension=dimension,
            pin_type=pin_type,
        )

        pin_in.additional_properties = d
        return pin_in

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
