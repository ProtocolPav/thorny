from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LocationCustomization")


@_attrs_define
class LocationCustomization:
    """
    Attributes:
        coordinates (list[int]): The coordinates Example: [200, 70, -43].
        horizontal_radius (int): The horizontal radius to check for (x and z axis) Example: 20.
        vertical_radius (int): The vertical radius to check for (y axis) Example: 3.
    """

    coordinates: list[int]
    horizontal_radius: int
    vertical_radius: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        coordinates = []
        for coordinates_item_data in self.coordinates:
            coordinates_item: int
            coordinates_item = coordinates_item_data
            coordinates.append(coordinates_item)

        horizontal_radius = self.horizontal_radius

        vertical_radius = self.vertical_radius

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "coordinates": coordinates,
                "horizontal_radius": horizontal_radius,
                "vertical_radius": vertical_radius,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        coordinates = []
        _coordinates = d.pop("coordinates")
        for coordinates_item_data in _coordinates:

            def _parse_coordinates_item(data: object) -> int:
                return cast(int, data)

            coordinates_item = _parse_coordinates_item(coordinates_item_data)

            coordinates.append(coordinates_item)

        horizontal_radius = d.pop("horizontal_radius")

        vertical_radius = d.pop("vertical_radius")

        location_customization = cls(
            coordinates=coordinates,
            horizontal_radius=horizontal_radius,
            vertical_radius=vertical_radius,
        )

        location_customization.additional_properties = d
        return location_customization

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
