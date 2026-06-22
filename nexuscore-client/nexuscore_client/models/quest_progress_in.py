from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="QuestProgressIn")


@_attrs_define
class QuestProgressIn:
    """
    Attributes:
        thorny_id (int): The ThornyID of the user
        quest_id (int): The ID of the quest
    """

    thorny_id: int
    quest_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thorny_id = self.thorny_id

        quest_id = self.quest_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thorny_id": thorny_id,
                "quest_id": quest_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        thorny_id = d.pop("thorny_id")

        quest_id = d.pop("quest_id")

        quest_progress_in = cls(
            thorny_id=thorny_id,
            quest_id=quest_id,
        )

        quest_progress_in.additional_properties = d
        return quest_progress_in

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
