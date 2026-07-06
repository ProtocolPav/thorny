from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.quest_progress_out_status import QuestProgressOutStatus

if TYPE_CHECKING:
    from ..models.objective_progress_out import ObjectiveProgressOut


T = TypeVar("T", bound="QuestProgressOut")


@_attrs_define
class QuestProgressOut:
    """
    Attributes:
        progress_id (int): The ID of the progress instance of the quest
        thorny_id (int): The ThornyID of the user
        quest_id (int): The ID of the quest
        accept_time (datetime.datetime): The time that the user accepted this quest
        start_time (datetime.datetime | None):
        end_time (datetime.datetime | None):
        status (QuestProgressOutStatus): The status of the quest
        objectives (list[ObjectiveProgressOut]):
    """

    progress_id: int
    thorny_id: int
    quest_id: int
    accept_time: datetime.datetime
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    status: QuestProgressOutStatus
    objectives: list[ObjectiveProgressOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        progress_id = self.progress_id

        thorny_id = self.thorny_id

        quest_id = self.quest_id

        accept_time = self.accept_time.isoformat()

        start_time: None | str
        if isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        end_time: None | str
        if isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        status = self.status.value

        objectives = []
        for objectives_item_data in self.objectives:
            objectives_item = objectives_item_data.to_dict()
            objectives.append(objectives_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "progress_id": progress_id,
                "thorny_id": thorny_id,
                "quest_id": quest_id,
                "accept_time": accept_time,
                "start_time": start_time,
                "end_time": end_time,
                "status": status,
                "objectives": objectives,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.objective_progress_out import ObjectiveProgressOut

        d = dict(src_dict)
        progress_id = d.pop("progress_id")

        thorny_id = d.pop("thorny_id")

        quest_id = d.pop("quest_id")

        accept_time = datetime.datetime.fromisoformat(d.pop("accept_time"))

        def _parse_start_time(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0_type_0 = datetime.datetime.fromisoformat(data)

                return start_time_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        start_time = _parse_start_time(d.pop("start_time"))

        def _parse_end_time(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0_type_0 = datetime.datetime.fromisoformat(data)

                return end_time_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        end_time = _parse_end_time(d.pop("end_time"))

        status = QuestProgressOutStatus(d.pop("status"))

        objectives = []
        _objectives = d.pop("objectives")
        for objectives_item_data in _objectives:
            objectives_item = ObjectiveProgressOut.from_dict(objectives_item_data)

            objectives.append(objectives_item)

        quest_progress_out = cls(
            progress_id=progress_id,
            thorny_id=thorny_id,
            quest_id=quest_id,
            accept_time=accept_time,
            start_time=start_time,
            end_time=end_time,
            status=status,
            objectives=objectives,
        )

        quest_progress_out.additional_properties = d
        return quest_progress_out

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
