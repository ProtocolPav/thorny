from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScriptEventTargetProgressModel")


@_attrs_define
class ScriptEventTargetProgressModel:
    """
    Attributes:
        target_type (Literal['scriptevent']): The type of the target. Must be equal to `objective_type`.
        target_uuid (Union[Unset, str]): The target uuid
        count (Union[Unset, int]): The number of Script ID's logged so far Default: 0. Example: 50.
    """

    target_type: Literal["scriptevent"]
    target_uuid: Union[Unset, str] = UNSET
    count: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        target_uuid = self.target_uuid

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_type": target_type,
            }
        )
        if target_uuid is not UNSET:
            field_dict["target_uuid"] = target_uuid
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_type = cast(Literal["scriptevent"], d.pop("target_type"))
        if target_type != "scriptevent":
            raise ValueError(f"target_type must match const 'scriptevent', got '{target_type}'")

        target_uuid = d.pop("target_uuid", UNSET)

        count = d.pop("count", UNSET)

        script_event_target_progress_model = cls(
            target_type=target_type,
            target_uuid=target_uuid,
            count=count,
        )

        script_event_target_progress_model.additional_properties = d
        return script_event_target_progress_model

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
