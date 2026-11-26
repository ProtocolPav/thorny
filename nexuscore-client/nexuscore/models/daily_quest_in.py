from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.objective_in import ObjectiveIn


T = TypeVar("T", bound="DailyQuestIn")


@_attrs_define
class DailyQuestIn:
    """A generated daily quest. Only the generator creates these; QuestIn does not accept `daily`.

    Attributes:
        start_time (datetime.datetime): The time that this quest begins to be able to be accepted
        end_time (datetime.datetime): The time that this quest will no longer be available to be accepted
        title (str): The quest title
        description (str): The quest description
        tags (list[str]): A list of tags describing this quest
        created_by (int): The Thorny ID that created this quest
        objectives (list[ObjectiveIn]):
        quest_type (Literal['daily'] | Unset): Always `daily` Default: 'daily'.
    """

    start_time: datetime.datetime
    end_time: datetime.datetime
    title: str
    description: str
    tags: list[str]
    created_by: int
    objectives: list[ObjectiveIn]
    quest_type: Literal["daily"] | Unset = "daily"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        title = self.title

        description = self.description

        tags = self.tags

        created_by = self.created_by

        objectives = []
        for objectives_item_data in self.objectives:
            objectives_item = objectives_item_data.to_dict()
            objectives.append(objectives_item)

        quest_type = self.quest_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_time": start_time,
                "end_time": end_time,
                "title": title,
                "description": description,
                "tags": tags,
                "created_by": created_by,
                "objectives": objectives,
            }
        )
        if quest_type is not UNSET:
            field_dict["quest_type"] = quest_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.objective_in import ObjectiveIn

        d = dict(src_dict)
        start_time = datetime.datetime.fromisoformat(d.pop("start_time"))

        end_time = datetime.datetime.fromisoformat(d.pop("end_time"))

        title = d.pop("title")

        description = d.pop("description")

        tags = cast(list[str], d.pop("tags"))

        created_by = d.pop("created_by")

        objectives = []
        _objectives = d.pop("objectives")
        for objectives_item_data in _objectives:
            objectives_item = ObjectiveIn.from_dict(objectives_item_data)

            objectives.append(objectives_item)

        quest_type = cast(Literal["daily"] | Unset, d.pop("quest_type", UNSET))
        if quest_type != "daily" and not isinstance(quest_type, Unset):
            raise ValueError(f"quest_type must match const 'daily', got '{quest_type}'")

        daily_quest_in = cls(
            start_time=start_time,
            end_time=end_time,
            title=title,
            description=description,
            tags=tags,
            created_by=created_by,
            objectives=objectives,
            quest_type=quest_type,
        )

        daily_quest_in.additional_properties = d
        return daily_quest_in

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
