from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.objective_update import ObjectiveUpdate


T = TypeVar("T", bound="QuestUpdate")


@_attrs_define
class QuestUpdate:
    """
    Attributes:
        start_time (datetime.datetime | None | Unset):
        end_time (datetime.datetime | None | Unset):
        title (None | str | Unset):
        description (None | str | Unset):
        tags (list[str] | None | Unset):
        quest_type (None | str | Unset):
        created_by (int | None | Unset):
        objectives (list[ObjectiveUpdate] | None | Unset):
    """

    start_time: datetime.datetime | None | Unset = UNSET
    end_time: datetime.datetime | None | Unset = UNSET
    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    quest_type: None | str | Unset = UNSET
    created_by: int | None | Unset = UNSET
    objectives: list[ObjectiveUpdate] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time: None | str | Unset
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        end_time: None | str | Unset
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        quest_type: None | str | Unset
        if isinstance(self.quest_type, Unset):
            quest_type = UNSET
        else:
            quest_type = self.quest_type

        created_by: int | None | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        objectives: list[dict[str, Any]] | None | Unset
        if isinstance(self.objectives, Unset):
            objectives = UNSET
        elif isinstance(self.objectives, list):
            objectives = []
            for objectives_type_0_item_data in self.objectives:
                objectives_type_0_item = objectives_type_0_item_data.to_dict()
                objectives.append(objectives_type_0_item)

        else:
            objectives = self.objectives

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if quest_type is not UNSET:
            field_dict["quest_type"] = quest_type
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if objectives is not UNSET:
            field_dict["objectives"] = objectives

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.objective_update import ObjectiveUpdate

        d = dict(src_dict)

        def _parse_start_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = datetime.datetime.fromisoformat(data)

                return start_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_end_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = datetime.datetime.fromisoformat(data)

                return end_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_quest_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        quest_type = _parse_quest_type(d.pop("quest_type", UNSET))

        def _parse_created_by(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_objectives(data: object) -> list[ObjectiveUpdate] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                objectives_type_0 = []
                _objectives_type_0 = data
                for objectives_type_0_item_data in _objectives_type_0:
                    objectives_type_0_item = ObjectiveUpdate.from_dict(objectives_type_0_item_data)

                    objectives_type_0.append(objectives_type_0_item)

                return objectives_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ObjectiveUpdate] | None | Unset, data)

        objectives = _parse_objectives(d.pop("objectives", UNSET))

        quest_update = cls(
            start_time=start_time,
            end_time=end_time,
            title=title,
            description=description,
            tags=tags,
            quest_type=quest_type,
            created_by=created_by,
            objectives=objectives,
        )

        quest_update.additional_properties = d
        return quest_update

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
