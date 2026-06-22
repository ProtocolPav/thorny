from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorldUpdate")


@_attrs_define
class WorldUpdate:
    """
    Attributes:
        overworld_border (Union[None, Unset, float]):
        nether_border (Union[None, Unset, float]):
        end_border (Union[None, Unset, float]):
    """

    overworld_border: Union[None, Unset, float] = UNSET
    nether_border: Union[None, Unset, float] = UNSET
    end_border: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        overworld_border: Union[None, Unset, float]
        if isinstance(self.overworld_border, Unset):
            overworld_border = UNSET
        else:
            overworld_border = self.overworld_border

        nether_border: Union[None, Unset, float]
        if isinstance(self.nether_border, Unset):
            nether_border = UNSET
        else:
            nether_border = self.nether_border

        end_border: Union[None, Unset, float]
        if isinstance(self.end_border, Unset):
            end_border = UNSET
        else:
            end_border = self.end_border

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if overworld_border is not UNSET:
            field_dict["overworld_border"] = overworld_border
        if nether_border is not UNSET:
            field_dict["nether_border"] = nether_border
        if end_border is not UNSET:
            field_dict["end_border"] = end_border

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_overworld_border(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        overworld_border = _parse_overworld_border(d.pop("overworld_border", UNSET))

        def _parse_nether_border(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        nether_border = _parse_nether_border(d.pop("nether_border", UNSET))

        def _parse_end_border(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        end_border = _parse_end_border(d.pop("end_border", UNSET))

        world_update = cls(
            overworld_border=overworld_border,
            nether_border=nether_border,
            end_border=end_border,
        )

        world_update.additional_properties = d
        return world_update

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
