from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="KillTargetModel")


@_attrs_define
class KillTargetModel:
    """
    Attributes:
        target_type (Literal['kill']): The type of the target. Must be equal to `objective_type`.
        count (int): The number of entities to be killed Example: 50.
        entity (str): The entity to be killed Example: minecraft:skeleton.
        target_uuid (Union[Unset, str]): The target uuid
    """

    target_type: Literal["kill"]
    count: int
    entity: str
    target_uuid: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_type = self.target_type

        count = self.count

        entity = self.entity

        target_uuid = self.target_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_type": target_type,
                "count": count,
                "entity": entity,
            }
        )
        if target_uuid is not UNSET:
            field_dict["target_uuid"] = target_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_type = cast(Literal["kill"], d.pop("target_type"))
        if target_type != "kill":
            raise ValueError(f"target_type must match const 'kill', got '{target_type}'")

        count = d.pop("count")

        entity = d.pop("entity")

        target_uuid = d.pop("target_uuid", UNSET)

        kill_target_model = cls(
            target_type=target_type,
            count=count,
            entity=entity,
            target_uuid=target_uuid,
        )

        kill_target_model.additional_properties = d
        return kill_target_model

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
