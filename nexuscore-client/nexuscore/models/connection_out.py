from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.connection_out_type import ConnectionOutType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectionOut")


@_attrs_define
class ConnectionOut:
    """
    Attributes:
        connection_id (int): The ID of the connection
        type_ (ConnectionOutType): The type of connection
        thorny_id (int): The ThornyID of the user
        time (datetime.datetime): The time of the connection
        ignored (bool | Unset): Whether the connection is ignored in metrics Default: False.
    """

    connection_id: int
    type_: ConnectionOutType
    thorny_id: int
    time: datetime.datetime
    ignored: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connection_id = self.connection_id

        type_ = self.type_.value

        thorny_id = self.thorny_id

        time = self.time.isoformat()

        ignored = self.ignored

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connection_id": connection_id,
                "type": type_,
                "thorny_id": thorny_id,
                "time": time,
            }
        )
        if ignored is not UNSET:
            field_dict["ignored"] = ignored

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = d.pop("connection_id")

        type_ = ConnectionOutType(d.pop("type"))

        thorny_id = d.pop("thorny_id")

        time = datetime.datetime.fromisoformat(d.pop("time"))

        ignored = d.pop("ignored", UNSET)

        connection_out = cls(
            connection_id=connection_id,
            type_=type_,
            thorny_id=thorny_id,
            time=time,
            ignored=ignored,
        )

        connection_out.additional_properties = d
        return connection_out

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
