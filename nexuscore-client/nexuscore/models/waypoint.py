from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.waypoint_waypoint_type import WaypointWaypointType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Waypoint")


@_attrs_define
class Waypoint:
    """
    Attributes:
        coordinates (list[int]): The coordinates to show the waypoint at
        waypoint_type (WaypointWaypointType): The type of waypoint to show
        dimension (str | Unset): The dimension to show the waypoint in Default: 'minecraft:overworld'.
    """

    coordinates: list[int]
    waypoint_type: WaypointWaypointType
    dimension: str | Unset = "minecraft:overworld"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        coordinates = []
        for coordinates_item_data in self.coordinates:
            coordinates_item: int
            coordinates_item = coordinates_item_data
            coordinates.append(coordinates_item)

        waypoint_type = self.waypoint_type.value

        dimension = self.dimension

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "coordinates": coordinates,
                "waypoint_type": waypoint_type,
            }
        )
        if dimension is not UNSET:
            field_dict["dimension"] = dimension

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

        waypoint_type = WaypointWaypointType(d.pop("waypoint_type"))

        dimension = d.pop("dimension", UNSET)

        waypoint = cls(
            coordinates=coordinates,
            waypoint_type=waypoint_type,
            dimension=dimension,
        )

        waypoint.additional_properties = d
        return waypoint

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
