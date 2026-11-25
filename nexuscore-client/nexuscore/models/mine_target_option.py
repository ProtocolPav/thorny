from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.random_count import RandomCount


T = TypeVar("T", bound="MineTargetOption")


@_attrs_define
class MineTargetOption:
    """
    Attributes:
        target_type (Literal['mine']): The type of the target. Must be equal to `objective_type`.
        block (str): The block to be mined Example: minecraft:dirt.
        target_uuid (str | Unset): The target uuid
        count (RandomCount | Unset): A randomizable number. Either an inclusive `min`/`max` range, or a list of
            `choices`.
    """

    target_type: Literal["mine"]
    block: str
    target_uuid: str | Unset = UNSET
    count: RandomCount | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        block = self.block

        target_uuid = self.target_uuid

        count: dict[str, Any] | Unset = UNSET
        if not isinstance(self.count, Unset):
            count = self.count.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_type": target_type,
                "block": block,
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
        target_type = cast(Literal["mine"], d.pop("target_type"))
        if target_type != "mine":
            raise ValueError(f"target_type must match const 'mine', got '{target_type}'")

        block = d.pop("block")

        target_uuid = d.pop("target_uuid", UNSET)

        _count = d.pop("count", UNSET)
        count: RandomCount | Unset
        if isinstance(_count, Unset):
            count = UNSET
        else:
            count = RandomCount.from_dict(_count)

        mine_target_option = cls(
            target_type=target_type,
            block=block,
            target_uuid=target_uuid,
            count=count,
        )

        mine_target_option.additional_properties = d
        return mine_target_option

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
