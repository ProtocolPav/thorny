from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location_customization import LocationCustomization


T = TypeVar("T", bound="LocationOption")


@_attrs_define
class LocationOption:
    """
    Attributes:
        chance (float): The chance (0 to 1) of this customization being added to the generated quest
        locations (list[LocationCustomization]): The locations to choose from
        show_waypoint (bool | Unset): Also add a waypoint at the chosen location Default: True.
    """

    chance: float
    locations: list[LocationCustomization]
    show_waypoint: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chance = self.chance

        locations = []
        for locations_item_data in self.locations:
            locations_item = locations_item_data.to_dict()
            locations.append(locations_item)

        show_waypoint = self.show_waypoint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chance": chance,
                "locations": locations,
            }
        )
        if show_waypoint is not UNSET:
            field_dict["show_waypoint"] = show_waypoint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location_customization import LocationCustomization

        d = dict(src_dict)
        chance = d.pop("chance")

        locations = []
        _locations = d.pop("locations")
        for locations_item_data in _locations:
            locations_item = LocationCustomization.from_dict(locations_item_data)

            locations.append(locations_item)

        show_waypoint = d.pop("show_waypoint", UNSET)

        location_option = cls(
            chance=chance,
            locations=locations,
            show_waypoint=show_waypoint,
        )

        location_option.additional_properties = d
        return location_option

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
