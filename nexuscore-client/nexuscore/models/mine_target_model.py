from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MineTargetModel")


@_attrs_define
class MineTargetModel:
    """
    Attributes:
        target_type (Literal['mine']): The type of the target. Must be equal to `objective_type`.
        count (int): The number of blocks to be mined Example: 50.
        block (str): The block to be mined Example: minecraft:dirt.
        target_uuid (str | Unset): The target uuid
    """

    target_type: Literal["mine"]
    count: int
    block: str
    target_uuid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        count = self.count

        block = self.block

        target_uuid = self.target_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_type": target_type,
                "count": count,
                "block": block,
            }
        )
        if target_uuid is not UNSET:
            field_dict["target_uuid"] = target_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_type = cast(Literal["mine"], d.pop("target_type"))
        if target_type != "mine":
            raise ValueError(f"target_type must match const 'mine', got '{target_type}'")

        count = d.pop("count")

        block = d.pop("block")

        target_uuid = d.pop("target_uuid", UNSET)

        mine_target_model = cls(
            target_type=target_type,
            count=count,
            block=block,
            target_uuid=target_uuid,
        )

        mine_target_model.additional_properties = d
        return mine_target_model

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
