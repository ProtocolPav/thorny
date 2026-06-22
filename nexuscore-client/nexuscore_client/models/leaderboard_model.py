from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.leaderboard_entry import LeaderboardEntry


T = TypeVar("T", bound="LeaderboardModel")


@_attrs_define
class LeaderboardModel:
    """
    Attributes:
        leaderboard (list['LeaderboardEntry']):
    """

    leaderboard: list["LeaderboardEntry"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        leaderboard = []
        for leaderboard_item_data in self.leaderboard:
            leaderboard_item = leaderboard_item_data.to_dict()
            leaderboard.append(leaderboard_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "leaderboard": leaderboard,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.leaderboard_entry import LeaderboardEntry

        d = dict(src_dict)
        leaderboard = []
        _leaderboard = d.pop("leaderboard")
        for leaderboard_item_data in _leaderboard:
            leaderboard_item = LeaderboardEntry.from_dict(leaderboard_item_data)

            leaderboard.append(leaderboard_item)

        leaderboard_model = cls(
            leaderboard=leaderboard,
        )

        leaderboard_model.additional_properties = d
        return leaderboard_model

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
