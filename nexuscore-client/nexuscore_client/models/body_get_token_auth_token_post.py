from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyGetTokenAuthTokenPost")


@_attrs_define
class BodyGetTokenAuthTokenPost:
    """
    Attributes:
        grant_type (Union[Unset, str]): The grant type, always `client_credentials` Default: 'client_credentials'.
        scope (Union[Unset, str]): The scopes to request. Leave empty for all available scopes. Default: ''.
        guild_id (Union[None, Unset, int]): The guild ID to request a token for.
            > [!warning]
            > Used only for master clients looking to perform guild-scoped actions.
        client_id (Union[None, Unset, str]): The client ID
        client_secret (Union[None, Unset, str]): The raw client secret
    """

    grant_type: Union[Unset, str] = "client_credentials"
    scope: Union[Unset, str] = ""
    guild_id: Union[None, Unset, int] = UNSET
    client_id: Union[None, Unset, str] = UNSET
    client_secret: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grant_type = self.grant_type

        scope = self.scope

        guild_id: Union[None, Unset, int]
        if isinstance(self.guild_id, Unset):
            guild_id = UNSET
        else:
            guild_id = self.guild_id

        client_id: Union[None, Unset, str]
        if isinstance(self.client_id, Unset):
            client_id = UNSET
        else:
            client_id = self.client_id

        client_secret: Union[None, Unset, str]
        if isinstance(self.client_secret, Unset):
            client_secret = UNSET
        else:
            client_secret = self.client_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if grant_type is not UNSET:
            field_dict["grant_type"] = grant_type
        if scope is not UNSET:
            field_dict["scope"] = scope
        if guild_id is not UNSET:
            field_dict["guild_id"] = guild_id
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grant_type = d.pop("grant_type", UNSET)

        scope = d.pop("scope", UNSET)

        def _parse_guild_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        guild_id = _parse_guild_id(d.pop("guild_id", UNSET))

        def _parse_client_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        client_id = _parse_client_id(d.pop("client_id", UNSET))

        def _parse_client_secret(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        client_secret = _parse_client_secret(d.pop("client_secret", UNSET))

        body_get_token_auth_token_post = cls(
            grant_type=grant_type,
            scope=scope,
            guild_id=guild_id,
            client_id=client_id,
            client_secret=client_secret,
        )

        body_get_token_auth_token_post.additional_properties = d
        return body_get_token_auth_token_post

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
