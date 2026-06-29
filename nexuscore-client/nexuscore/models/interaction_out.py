from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.interaction_out_type import InteractionOutType

T = TypeVar("T", bound="InteractionOut")


@_attrs_define
class InteractionOut:
    """
    Attributes:
        interaction_id (int): The ID of the interaction
        thorny_id (int): The ThornyID of the user
        type_ (InteractionOutType): The type of interaction
        coordinates (list[int]): The coordinates of the interaction
        reference (str): The reference of the interaction
        mainhand (None | str):
        time (datetime.datetime): The time of the interaction
        dimension (str): The dimension of the interaction
    """

    interaction_id: int
    thorny_id: int
    type_: InteractionOutType
    coordinates: list[int]
    reference: str
    mainhand: None | str
    time: datetime.datetime
    dimension: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interaction_id = self.interaction_id

        thorny_id = self.thorny_id

        type_ = self.type_.value

        coordinates = []
        for coordinates_item_data in self.coordinates:
            coordinates_item: int
            coordinates_item = coordinates_item_data
            coordinates.append(coordinates_item)

        reference = self.reference

        mainhand: None | str
        mainhand = self.mainhand

        time = self.time.isoformat()

        dimension = self.dimension

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interaction_id": interaction_id,
                "thorny_id": thorny_id,
                "type": type_,
                "coordinates": coordinates,
                "reference": reference,
                "mainhand": mainhand,
                "time": time,
                "dimension": dimension,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interaction_id = d.pop("interaction_id")

        thorny_id = d.pop("thorny_id")

        type_ = InteractionOutType(d.pop("type"))

        coordinates = []
        _coordinates = d.pop("coordinates")
        for coordinates_item_data in _coordinates:

            def _parse_coordinates_item(data: object) -> int:
                return cast(int, data)

            coordinates_item = _parse_coordinates_item(coordinates_item_data)

            coordinates.append(coordinates_item)

        reference = d.pop("reference")

        def _parse_mainhand(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mainhand = _parse_mainhand(d.pop("mainhand"))

        time = datetime.datetime.fromisoformat(d.pop("time"))

        dimension = d.pop("dimension")

        interaction_out = cls(
            interaction_id=interaction_id,
            thorny_id=thorny_id,
            type_=type_,
            coordinates=coordinates,
            reference=reference,
            mainhand=mainhand,
            time=time,
            dimension=dimension,
        )

        interaction_out.additional_properties = d
        return interaction_out

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
