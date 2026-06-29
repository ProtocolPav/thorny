from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.objective_progress_out_status import ObjectiveProgressOutStatus

if TYPE_CHECKING:
    from ..models.customization_progress import CustomizationProgress
    from ..models.kill_target_progress_model import KillTargetProgressModel
    from ..models.mine_target_progress_model import MineTargetProgressModel
    from ..models.script_event_target_progress_model import ScriptEventTargetProgressModel


T = TypeVar("T", bound="ObjectiveProgressOut")


@_attrs_define
class ObjectiveProgressOut:
    """
    Attributes:
        progress_id (int): The quest progress ID
        objective_id (int): The objective ID
        start_time (datetime.datetime | None):
        end_time (datetime.datetime | None):
        status (ObjectiveProgressOutStatus): The status of this objective
        target_progress (list[KillTargetProgressModel | MineTargetProgressModel | ScriptEventTargetProgressModel]): List
            of each objective target's progress
        customization_progress (CustomizationProgress):
    """

    progress_id: int
    objective_id: int
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    status: ObjectiveProgressOutStatus
    target_progress: list[KillTargetProgressModel | MineTargetProgressModel | ScriptEventTargetProgressModel]
    customization_progress: CustomizationProgress
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.kill_target_progress_model import KillTargetProgressModel
        from ..models.mine_target_progress_model import MineTargetProgressModel

        progress_id = self.progress_id

        objective_id = self.objective_id

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

        target_progress = []
        for target_progress_item_data in self.target_progress:
            target_progress_item: dict[str, Any]
            if isinstance(target_progress_item_data, MineTargetProgressModel):
                target_progress_item = target_progress_item_data.to_dict()
            elif isinstance(target_progress_item_data, KillTargetProgressModel):
                target_progress_item = target_progress_item_data.to_dict()
            else:
                target_progress_item = target_progress_item_data.to_dict()

            target_progress.append(target_progress_item)

        customization_progress = self.customization_progress.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "progress_id": progress_id,
                "objective_id": objective_id,
                "start_time": start_time,
                "end_time": end_time,
                "status": status,
                "target_progress": target_progress,
                "customization_progress": customization_progress,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customization_progress import CustomizationProgress
        from ..models.kill_target_progress_model import KillTargetProgressModel
        from ..models.mine_target_progress_model import MineTargetProgressModel
        from ..models.script_event_target_progress_model import ScriptEventTargetProgressModel

        d = dict(src_dict)
        progress_id = d.pop("progress_id")

        objective_id = d.pop("objective_id")

        def _parse_start_time(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = datetime.datetime.fromisoformat(data)

                return start_time_type_0
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
                end_time_type_0 = datetime.datetime.fromisoformat(data)

                return end_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        end_time = _parse_end_time(d.pop("end_time"))

        status = ObjectiveProgressOutStatus(d.pop("status"))

        target_progress = []
        _target_progress = d.pop("target_progress")
        for target_progress_item_data in _target_progress:

            def _parse_target_progress_item(
                data: object,
            ) -> KillTargetProgressModel | MineTargetProgressModel | ScriptEventTargetProgressModel:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    target_progress_item_type_0 = MineTargetProgressModel.from_dict(data)

                    return target_progress_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    target_progress_item_type_1 = KillTargetProgressModel.from_dict(data)

                    return target_progress_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                target_progress_item_type_2 = ScriptEventTargetProgressModel.from_dict(data)

                return target_progress_item_type_2

            target_progress_item = _parse_target_progress_item(target_progress_item_data)

            target_progress.append(target_progress_item)

        customization_progress = CustomizationProgress.from_dict(d.pop("customization_progress"))

        objective_progress_out = cls(
            progress_id=progress_id,
            objective_id=objective_id,
            start_time=start_time,
            end_time=end_time,
            status=status,
            target_progress=target_progress,
            customization_progress=customization_progress,
        )

        objective_progress_out.additional_properties = d
        return objective_progress_out

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
