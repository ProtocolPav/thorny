from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorldOut")


@_attrs_define
class WorldOut:
    """
    Attributes:
        guild_id (int): The guild ID that corresponds to this world
        overworld_border (float): The Overworld border size
        nether_border (float): The Nether border size
        end_border (float): The End border size
    """

    guild_id: int
    overworld_border: float
    nether_border: float
    end_border: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        guild_id = self.guild_id

        overworld_border = self.overworld_border

        nether_border = self.nether_border

        end_border = self.end_border

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "guild_id": guild_id,
                "overworld_border": overworld_border,
                "nether_border": nether_border,
                "end_border": end_border,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        guild_id = d.pop("guild_id")

        overworld_border = d.pop("overworld_border")

        nether_border = d.pop("nether_border")

        end_border = d.pop("end_border")

        world_out = cls(
            guild_id=guild_id,
            overworld_border=overworld_border,
            nether_border=nether_border,
            end_border=end_border,
        )

        world_out.additional_properties = d
        return world_out

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
