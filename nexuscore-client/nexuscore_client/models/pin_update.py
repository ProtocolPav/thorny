from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PinUpdate")


@_attrs_define
class PinUpdate:
    """
    Attributes:
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        coordinates (Union[None, Unset, list[int]]):
        dimension (Union[None, Unset, str]):
        pin_type (Union[None, Unset, str]):
    """

    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    coordinates: Union[None, Unset, list[int]] = UNSET
    dimension: Union[None, Unset, str] = UNSET
    pin_type: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        coordinates: Union[None, Unset, list[int]]
        if isinstance(self.coordinates, Unset):
            coordinates = UNSET
        elif isinstance(self.coordinates, list):
            coordinates = self.coordinates

        else:
            coordinates = self.coordinates

        dimension: Union[None, Unset, str]
        if isinstance(self.dimension, Unset):
            dimension = UNSET
        else:
            dimension = self.dimension

        pin_type: Union[None, Unset, str]
        if isinstance(self.pin_type, Unset):
            pin_type = UNSET
        else:
            pin_type = self.pin_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates
        if dimension is not UNSET:
            field_dict["dimension"] = dimension
        if pin_type is not UNSET:
            field_dict["pin_type"] = pin_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_coordinates(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                coordinates_type_0 = cast(list[int], data)

                return coordinates_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        coordinates = _parse_coordinates(d.pop("coordinates", UNSET))

        def _parse_dimension(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dimension = _parse_dimension(d.pop("dimension", UNSET))

        def _parse_pin_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pin_type = _parse_pin_type(d.pop("pin_type", UNSET))

        pin_update = cls(
            name=name,
            description=description,
            coordinates=coordinates,
            dimension=dimension,
            pin_type=pin_type,
        )

        pin_update.additional_properties = d
        return pin_update

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
