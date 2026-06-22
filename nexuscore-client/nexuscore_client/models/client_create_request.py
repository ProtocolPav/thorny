from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scope import Scope

T = TypeVar("T", bound="ClientCreateRequest")


@_attrs_define
class ClientCreateRequest:
    """
    Attributes:
        client_name (str): The name of the client
        guild_id (int): The guild ID of the client
        scopes (list[Scope]): The requested scopes of the client
    """

    client_name: str
    guild_id: int
    scopes: list[Scope]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_name = self.client_name

        guild_id = self.guild_id

        scopes = []
        for scopes_item_data in self.scopes:
            scopes_item = scopes_item_data.value
            scopes.append(scopes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_name": client_name,
                "guild_id": guild_id,
                "scopes": scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_name = d.pop("client_name")

        guild_id = d.pop("guild_id")

        scopes = []
        _scopes = d.pop("scopes")
        for scopes_item_data in _scopes:
            scopes_item = Scope(scopes_item_data)

            scopes.append(scopes_item)

        client_create_request = cls(
            client_name=client_name,
            guild_id=guild_id,
            scopes=scopes,
        )

        client_create_request.additional_properties = d
        return client_create_request

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
