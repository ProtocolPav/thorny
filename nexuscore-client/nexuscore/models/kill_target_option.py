from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.random_count import RandomCount


T = TypeVar("T", bound="KillTargetOption")


@_attrs_define
class KillTargetOption:
    """
    Attributes:
        target_type (Literal['kill']): The type of the target. Must be equal to `objective_type`.
        entity (str): The entity to be killed Example: minecraft:skeleton.
        target_uuid (str | Unset): The target uuid
        count (RandomCount | Unset): A randomizable number. Either an inclusive `min`/`max` range, or a list of
            `choices`.
    """

    target_type: Literal["kill"]
    entity: str
    target_uuid: str | Unset = UNSET
    count: RandomCount | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        entity = self.entity

        target_uuid = self.target_uuid

        count: dict[str, Any] | Unset = UNSET
        if not isinstance(self.count, Unset):
            count = self.count.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_type": target_type,
                "entity": entity,
            }
        )
        if target_uuid is not UNSET:
            field_dict["target_uuid"] = target_uuid
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.random_count import RandomCount

        d = dict(src_dict)
        target_type = cast(Literal["kill"], d.pop("target_type"))
        if target_type != "kill":
            raise ValueError(f"target_type must match const 'kill', got '{target_type}'")

        entity = d.pop("entity")

        target_uuid = d.pop("target_uuid", UNSET)

        _count = d.pop("count", UNSET)
        count: RandomCount | Unset
        if isinstance(_count, Unset):
            count = UNSET
        else:
            count = RandomCount.from_dict(_count)

        kill_target_option = cls(
            target_type=target_type,
            entity=entity,
            target_uuid=target_uuid,
            count=count,
        )

        kill_target_option.additional_properties = d
        return kill_target_option

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
