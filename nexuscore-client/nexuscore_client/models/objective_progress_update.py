import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.objective_progress_update_status_type_0 import ObjectiveProgressUpdateStatusType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customization_progress import CustomizationProgress
    from ..models.kill_target_progress_model import KillTargetProgressModel
    from ..models.mine_target_progress_model import MineTargetProgressModel
    from ..models.script_event_target_progress_model import ScriptEventTargetProgressModel


T = TypeVar("T", bound="ObjectiveProgressUpdate")


@_attrs_define
class ObjectiveProgressUpdate:
    """
    Attributes:
        objective_id (Union[None, Unset, int]):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):
        status (Union[None, ObjectiveProgressUpdateStatusType0, Unset]):
        target_progress (Union[None, Unset, list[Union['KillTargetProgressModel', 'MineTargetProgressModel',
            'ScriptEventTargetProgressModel']]]):
        customization_progress (Union['CustomizationProgress', None, Unset]):
    """

    objective_id: Union[None, Unset, int] = UNSET
    start_time: Union[None, Unset, datetime.datetime] = UNSET
    end_time: Union[None, Unset, datetime.datetime] = UNSET
    status: Union[None, ObjectiveProgressUpdateStatusType0, Unset] = UNSET
    target_progress: Union[
        None, Unset, list[Union["KillTargetProgressModel", "MineTargetProgressModel", "ScriptEventTargetProgressModel"]]
    ] = UNSET
    customization_progress: Union["CustomizationProgress", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customization_progress import CustomizationProgress
        from ..models.kill_target_progress_model import KillTargetProgressModel
        from ..models.mine_target_progress_model import MineTargetProgressModel

        objective_id: Union[None, Unset, int]
        if isinstance(self.objective_id, Unset):
            objective_id = UNSET
        else:
            objective_id = self.objective_id

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
        elif isinstance(self.status, ObjectiveProgressUpdateStatusType0):
            status = self.status.value
        else:
            status = self.status

        target_progress: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.target_progress, Unset):
            target_progress = UNSET
        elif isinstance(self.target_progress, list):
            target_progress = []
            for target_progress_type_0_item_data in self.target_progress:
                target_progress_type_0_item: dict[str, Any]
                if isinstance(target_progress_type_0_item_data, MineTargetProgressModel):
                    target_progress_type_0_item = target_progress_type_0_item_data.to_dict()
                elif isinstance(target_progress_type_0_item_data, KillTargetProgressModel):
                    target_progress_type_0_item = target_progress_type_0_item_data.to_dict()
                else:
                    target_progress_type_0_item = target_progress_type_0_item_data.to_dict()

                target_progress.append(target_progress_type_0_item)

        else:
            target_progress = self.target_progress

        customization_progress: Union[None, Unset, dict[str, Any]]
        if isinstance(self.customization_progress, Unset):
            customization_progress = UNSET
        elif isinstance(self.customization_progress, CustomizationProgress):
            customization_progress = self.customization_progress.to_dict()
        else:
            customization_progress = self.customization_progress

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if objective_id is not UNSET:
            field_dict["objective_id"] = objective_id
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if status is not UNSET:
            field_dict["status"] = status
        if target_progress is not UNSET:
            field_dict["target_progress"] = target_progress
        if customization_progress is not UNSET:
            field_dict["customization_progress"] = customization_progress

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customization_progress import CustomizationProgress
        from ..models.kill_target_progress_model import KillTargetProgressModel
        from ..models.mine_target_progress_model import MineTargetProgressModel
        from ..models.script_event_target_progress_model import ScriptEventTargetProgressModel

        d = dict(src_dict)

        def _parse_objective_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        objective_id = _parse_objective_id(d.pop("objective_id", UNSET))

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
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
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_status(data: object) -> Union[None, ObjectiveProgressUpdateStatusType0, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = ObjectiveProgressUpdateStatusType0(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ObjectiveProgressUpdateStatusType0, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_target_progress(
            data: object,
        ) -> Union[
            None,
            Unset,
            list[Union["KillTargetProgressModel", "MineTargetProgressModel", "ScriptEventTargetProgressModel"]],
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                target_progress_type_0 = []
                _target_progress_type_0 = data
                for target_progress_type_0_item_data in _target_progress_type_0:

                    def _parse_target_progress_type_0_item(
                        data: object,
                    ) -> Union["KillTargetProgressModel", "MineTargetProgressModel", "ScriptEventTargetProgressModel"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            target_progress_type_0_item_type_0 = MineTargetProgressModel.from_dict(data)

                            return target_progress_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            target_progress_type_0_item_type_1 = KillTargetProgressModel.from_dict(data)

                            return target_progress_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        target_progress_type_0_item_type_2 = ScriptEventTargetProgressModel.from_dict(data)

                        return target_progress_type_0_item_type_2

                    target_progress_type_0_item = _parse_target_progress_type_0_item(target_progress_type_0_item_data)

                    target_progress_type_0.append(target_progress_type_0_item)

                return target_progress_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    Unset,
                    list[Union["KillTargetProgressModel", "MineTargetProgressModel", "ScriptEventTargetProgressModel"]],
                ],
                data,
            )

        target_progress = _parse_target_progress(d.pop("target_progress", UNSET))

        def _parse_customization_progress(data: object) -> Union["CustomizationProgress", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                customization_progress_type_0 = CustomizationProgress.from_dict(data)

                return customization_progress_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CustomizationProgress", None, Unset], data)

        customization_progress = _parse_customization_progress(d.pop("customization_progress", UNSET))

        objective_progress_update = cls(
            objective_id=objective_id,
            start_time=start_time,
            end_time=end_time,
            status=status,
            target_progress=target_progress,
            customization_progress=customization_progress,
        )

        objective_progress_update.additional_properties = d
        return objective_progress_update

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
