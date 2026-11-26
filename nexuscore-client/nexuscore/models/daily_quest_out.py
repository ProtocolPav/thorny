from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.quest_out import QuestOut


T = TypeVar("T", bound="DailyQuestOut")


@_attrs_define
class DailyQuestOut:
    """
    Attributes:
        quest_date (datetime.date): The UTC date this daily quest is for
        template_id (int | None): The template this quest was generated from. `null` if the template was deleted.
        quest (QuestOut):
    """

    quest_date: datetime.date
    template_id: int | None
    quest: QuestOut
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        quest_date = self.quest_date.isoformat()

        template_id: int | None
        template_id = self.template_id

        quest = self.quest.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "quest_date": quest_date,
                "template_id": template_id,
                "quest": quest,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.quest_out import QuestOut

        d = dict(src_dict)
        quest_date = datetime.date.fromisoformat(d.pop("quest_date"))

        def _parse_template_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        template_id = _parse_template_id(d.pop("template_id"))

        quest = QuestOut.from_dict(d.pop("quest"))

        daily_quest_out = cls(
            quest_date=quest_date,
            template_id=template_id,
            quest=quest,
        )

        daily_quest_out.additional_properties = d
        return daily_quest_out

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
