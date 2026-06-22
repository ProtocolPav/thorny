from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.interaction_in_type import InteractionInType

T = TypeVar("T", bound="InteractionIn")


@_attrs_define
class InteractionIn:
    """
    Attributes:
        thorny_id (int): The ThornyID of the user
        type_ (InteractionInType): The type of interaction
        coordinates (list[int]): The coordinates of the interaction
        reference (str): The reference of the interaction
        mainhand (Union[None, str]):
        dimension (str): The dimension of the interaction
    """

    thorny_id: int
    type_: InteractionInType
    coordinates: list[int]
    reference: str
    mainhand: Union[None, str]
    dimension: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thorny_id = self.thorny_id

        type_ = self.type_.value

        coordinates = []
        for coordinates_item_data in self.coordinates:
            coordinates_item: int
            coordinates_item = coordinates_item_data
            coordinates.append(coordinates_item)

        reference = self.reference

        mainhand: Union[None, str]
        mainhand = self.mainhand

        dimension = self.dimension

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thorny_id": thorny_id,
                "type": type_,
                "coordinates": coordinates,
                "reference": reference,
                "mainhand": mainhand,
                "dimension": dimension,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        thorny_id = d.pop("thorny_id")

        type_ = InteractionInType(d.pop("type"))

        coordinates = []
        _coordinates = d.pop("coordinates")
        for coordinates_item_data in _coordinates:

            def _parse_coordinates_item(data: object) -> int:
                return cast(int, data)

            coordinates_item = _parse_coordinates_item(coordinates_item_data)

            coordinates.append(coordinates_item)

        reference = d.pop("reference")

        def _parse_mainhand(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mainhand = _parse_mainhand(d.pop("mainhand"))

        dimension = d.pop("dimension")

        interaction_in = cls(
            thorny_id=thorny_id,
            type_=type_,
            coordinates=coordinates,
            reference=reference,
            mainhand=mainhand,
            dimension=dimension,
        )

        interaction_in.additional_properties = d
        return interaction_in

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
