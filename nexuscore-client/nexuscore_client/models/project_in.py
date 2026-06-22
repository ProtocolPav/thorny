from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectIn")


@_attrs_define
class ProjectIn:
    """
    Attributes:
        owner_id (int): The project owner ID
        coordinates (list[int]): The coordinates of the project
        description (str): A short description of the project
        dimension (str): The dimension of the project
        name (str): The name of the project
        pin_id (int | None):
    """

    owner_id: int
    coordinates: list[int]
    description: str
    dimension: str
    name: str
    pin_id: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        coordinates = self.coordinates

        description = self.description

        dimension = self.dimension

        name = self.name

        pin_id: int | None
        pin_id = self.pin_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "owner_id": owner_id,
                "coordinates": coordinates,
                "description": description,
                "dimension": dimension,
                "name": name,
                "pin_id": pin_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("owner_id")

        coordinates = cast(list[int], d.pop("coordinates"))

        description = d.pop("description")

        dimension = d.pop("dimension")

        name = d.pop("name")

        def _parse_pin_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        pin_id = _parse_pin_id(d.pop("pin_id"))

        project_in = cls(
            owner_id=owner_id,
            coordinates=coordinates,
            description=description,
            dimension=dimension,
            name=name,
            pin_id=pin_id,
        )

        project_in.additional_properties = d
        return project_in

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
