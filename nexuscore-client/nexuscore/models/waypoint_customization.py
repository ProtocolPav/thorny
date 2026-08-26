from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.waypoint import Waypoint


T = TypeVar("T", bound="WaypointCustomization")


@_attrs_define
class WaypointCustomization:
    """
    Attributes:
        waypoints (list[Waypoint]): The waypoints to show
    """

    waypoints: list[Waypoint]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        waypoints = []
        for waypoints_item_data in self.waypoints:
            waypoints_item = waypoints_item_data.to_dict()
            waypoints.append(waypoints_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "waypoints": waypoints,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.waypoint import Waypoint

        d = dict(src_dict)
        waypoints = []
        _waypoints = d.pop("waypoints")
        for waypoints_item_data in _waypoints:
            waypoints_item = Waypoint.from_dict(waypoints_item_data)

            waypoints.append(waypoints_item)

        waypoint_customization = cls(
            waypoints=waypoints,
        )

        waypoint_customization.additional_properties = d
        return waypoint_customization

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
