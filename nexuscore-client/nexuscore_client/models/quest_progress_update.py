import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.quest_progress_update_status_type_0 import QuestProgressUpdateStatusType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.objective_progress_update import ObjectiveProgressUpdate


T = TypeVar("T", bound="QuestProgressUpdate")


@_attrs_define
class QuestProgressUpdate:
    """
    Attributes:
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):
        status (Union[None, QuestProgressUpdateStatusType0, Unset]):
        objectives (Union[None, Unset, list['ObjectiveProgressUpdate']]):
    """

    start_time: Union[None, Unset, datetime.datetime] = UNSET
    end_time: Union[None, Unset, datetime.datetime] = UNSET
    status: Union[None, QuestProgressUpdateStatusType0, Unset] = UNSET
    objectives: Union[None, Unset, list["ObjectiveProgressUpdate"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time: Union[None, Unset, str]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        end_time: Union[None, Unset, str]
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, QuestProgressUpdateStatusType0):
            status = self.status.value
        else:
            status = self.status

        objectives: Union[None, Unset, list[dict[str, Any]]]
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
        if status is not UNSET:
            field_dict["status"] = status
        if objectives is not UNSET:
            field_dict["objectives"] = objectives

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.objective_progress_update import ObjectiveProgressUpdate

        d = dict(src_dict)

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0_type_0 = isoparse(data)

                return start_time_type_0_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_end_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0_type_0 = isoparse(data)

                return end_time_type_0_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_status(data: object) -> Union[None, QuestProgressUpdateStatusType0, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = QuestProgressUpdateStatusType0(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, QuestProgressUpdateStatusType0, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_objectives(data: object) -> Union[None, Unset, list["ObjectiveProgressUpdate"]]:
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
                    objectives_type_0_item = ObjectiveProgressUpdate.from_dict(objectives_type_0_item_data)

                    objectives_type_0.append(objectives_type_0_item)

                return objectives_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ObjectiveProgressUpdate"]], data)

        objectives = _parse_objectives(d.pop("objectives", UNSET))

        quest_progress_update = cls(
            start_time=start_time,
            end_time=end_time,
            status=status,
            objectives=objectives,
        )

        quest_progress_update.additional_properties = d
        return quest_progress_update

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
