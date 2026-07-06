from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScriptEventTargetModel")


@_attrs_define
class ScriptEventTargetModel:
    """
    Attributes:
        target_type (Literal['scriptevent']): The type of the target. Must be equal to `objective_type`.
        count (int): The number of ID's before this objective is completed Example: 50.
        script_id (str): The script_event ID which will trigger the objective Example: quest:button_1.
        target_uuid (str | Unset): The target uuid
    """

    target_type: Literal["scriptevent"]
    count: int
    script_id: str
    target_uuid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        count = self.count

        script_id = self.script_id

        target_uuid = self.target_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_type": target_type,
                "count": count,
                "script_id": script_id,
            }
        )
        if target_uuid is not UNSET:
            field_dict["target_uuid"] = target_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_type = cast(Literal["scriptevent"], d.pop("target_type"))
        if target_type != "scriptevent":
            raise ValueError(f"target_type must match const 'scriptevent', got '{target_type}'")

        count = d.pop("count")

        script_id = d.pop("script_id")

        target_uuid = d.pop("target_uuid", UNSET)

        script_event_target_model = cls(
            target_type=target_type,
            count=count,
            script_id=script_id,
            target_uuid=target_uuid,
        )

        script_event_target_model.additional_properties = d
        return script_event_target_model

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
