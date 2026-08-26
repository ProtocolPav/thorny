from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VisitTargetProgressModel")


@_attrs_define
class VisitTargetProgressModel:
    """
    Attributes:
        target_type (Literal['visit']):
        target_uuid (str | Unset): The target uuid
        count (int | Unset): The number of this target to be reached. At least 1. Default: 0. Example: 50.
        seconds (int | Unset): The number of seconds spent in the area so far Default: 0.
    """

    target_type: Literal["visit"]
    target_uuid: str | Unset = UNSET
    count: int | Unset = 0
    seconds: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        target_uuid = self.target_uuid

        count = self.count

        seconds = self.seconds

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
        if seconds is not UNSET:
            field_dict["seconds"] = seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_type = cast(Literal["visit"], d.pop("target_type"))
        if target_type != "visit":
            raise ValueError(f"target_type must match const 'visit', got '{target_type}'")

        target_uuid = d.pop("target_uuid", UNSET)

        count = d.pop("count", UNSET)

        seconds = d.pop("seconds", UNSET)

        visit_target_progress_model = cls(
            target_type=target_type,
            target_uuid=target_uuid,
            count=count,
            seconds=seconds,
        )

        visit_target_progress_model.additional_properties = d
        return visit_target_progress_model

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
