from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VisitTargetModel")


@_attrs_define
class VisitTargetModel:
    """
    Attributes:
        target_type (Literal['visit']): The type of the target. Must be equal to `objective_type`.
        count (int): The number of this target to be reached. At least 1. Example: 50.
        helper_text (str): The helper text to be shown to the player, after the verb 'Locate'
        coordinates (list[int]): The coordinates
        horizontal_radius (int): The horizontal radius to check for (x and z axis)
        target_uuid (str | Unset): The target uuid
        vertical_radius (int | None | Unset): The vertical radius to check for (y axis)
        seconds (int | Unset): The amount of seconds to stay in the area Default: 2.
    """

    target_type: Literal["visit"]
    count: int
    helper_text: str
    coordinates: list[int]
    horizontal_radius: int
    target_uuid: str | Unset = UNSET
    vertical_radius: int | None | Unset = UNSET
    seconds: int | Unset = 2
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        count = self.count

        helper_text = self.helper_text

        coordinates = []
        for coordinates_item_data in self.coordinates:
            coordinates_item: int
            coordinates_item = coordinates_item_data
            coordinates.append(coordinates_item)

        horizontal_radius = self.horizontal_radius

        target_uuid = self.target_uuid

        vertical_radius: int | None | Unset
        if isinstance(self.vertical_radius, Unset):
            vertical_radius = UNSET
        else:
            vertical_radius = self.vertical_radius

        seconds = self.seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_type": target_type,
                "count": count,
                "helper_text": helper_text,
                "coordinates": coordinates,
                "horizontal_radius": horizontal_radius,
            }
        )
        if target_uuid is not UNSET:
            field_dict["target_uuid"] = target_uuid
        if vertical_radius is not UNSET:
            field_dict["vertical_radius"] = vertical_radius
        if seconds is not UNSET:
            field_dict["seconds"] = seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_type = cast(Literal["visit"], d.pop("target_type"))
        if target_type != "visit":
            raise ValueError(f"target_type must match const 'visit', got '{target_type}'")

        count = d.pop("count")

        helper_text = d.pop("helper_text")

        coordinates = []
        _coordinates = d.pop("coordinates")
        for coordinates_item_data in _coordinates:

            def _parse_coordinates_item(data: object) -> int:
                return cast(int, data)

            coordinates_item = _parse_coordinates_item(coordinates_item_data)

            coordinates.append(coordinates_item)

        horizontal_radius = d.pop("horizontal_radius")

        target_uuid = d.pop("target_uuid", UNSET)

        def _parse_vertical_radius(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        vertical_radius = _parse_vertical_radius(d.pop("vertical_radius", UNSET))

        seconds = d.pop("seconds", UNSET)

        visit_target_model = cls(
            target_type=target_type,
            count=count,
            helper_text=helper_text,
            coordinates=coordinates,
            horizontal_radius=horizontal_radius,
            target_uuid=target_uuid,
            vertical_radius=vertical_radius,
            seconds=seconds,
        )

        visit_target_model.additional_properties = d
        return visit_target_model

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
