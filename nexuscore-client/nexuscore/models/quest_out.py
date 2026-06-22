from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.objective_out import ObjectiveOut
    from ..models.user_out import UserOut


T = TypeVar("T", bound="QuestOut")


@_attrs_define
class QuestOut:
    """
    Attributes:
        quest_id (int): The Quest ID
        start_time (datetime.datetime): The time that this quest begins to be able to be accepted
        end_time (datetime.datetime): The time that this quest will no longer be available to be accepted
        title (str): The quest title
        description (str): The quest description
        tags (list[str]): A list of tags describing this quest
        quest_type (str): The quest type
        created_by (UserOut):
        objectives (list[ObjectiveOut]):
    """

    quest_id: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    title: str
    description: str
    tags: list[str]
    quest_type: str
    created_by: UserOut
    objectives: list[ObjectiveOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        quest_id = self.quest_id

        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        title = self.title

        description = self.description

        tags = self.tags

        quest_type = self.quest_type

        created_by = self.created_by.to_dict()

        objectives = []
        for objectives_item_data in self.objectives:
            objectives_item = objectives_item_data.to_dict()
            objectives.append(objectives_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "quest_id": quest_id,
                "start_time": start_time,
                "end_time": end_time,
                "title": title,
                "description": description,
                "tags": tags,
                "quest_type": quest_type,
                "created_by": created_by,
                "objectives": objectives,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.objective_out import ObjectiveOut
        from ..models.user_out import UserOut

        d = dict(src_dict)
        quest_id = d.pop("quest_id")

        start_time = datetime.datetime.fromisoformat(d.pop("start_time"))

        end_time = datetime.datetime.fromisoformat(d.pop("end_time"))

        title = d.pop("title")

        description = d.pop("description")

        tags = cast(list[str], d.pop("tags"))

        quest_type = d.pop("quest_type")

        created_by = UserOut.from_dict(d.pop("created_by"))

        objectives = []
        _objectives = d.pop("objectives")
        for objectives_item_data in _objectives:
            objectives_item = ObjectiveOut.from_dict(objectives_item_data)

            objectives.append(objectives_item)

        quest_out = cls(
            quest_id=quest_id,
            start_time=start_time,
            end_time=end_time,
            title=title,
            description=description,
            tags=tags,
            quest_type=quest_type,
            created_by=created_by,
            objectives=objectives,
        )

        quest_out.additional_properties = d
        return quest_out

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
