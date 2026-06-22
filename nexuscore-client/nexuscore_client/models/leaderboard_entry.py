from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LeaderboardEntry")


@_attrs_define
class LeaderboardEntry:
    """
    Attributes:
        value (Union[float, int]): The value of the leaderboard, if it's playtime then it is seconds, etc.
        thorny_id (int):
        discord_id (int):
    """

    value: Union[float, int]
    thorny_id: int
    discord_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value: Union[float, int]
        value = self.value

        thorny_id = self.thorny_id

        discord_id = self.discord_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "thorny_id": thorny_id,
                "discord_id": discord_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_value(data: object) -> Union[float, int]:
            return cast(Union[float, int], data)

        value = _parse_value(d.pop("value"))

        thorny_id = d.pop("thorny_id")

        discord_id = d.pop("discord_id")

        leaderboard_entry = cls(
            value=value,
            thorny_id=thorny_id,
            discord_id=discord_id,
        )

        leaderboard_entry.additional_properties = d
        return leaderboard_entry

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
