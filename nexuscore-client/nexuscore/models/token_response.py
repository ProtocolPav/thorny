from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenResponse")


@_attrs_define
class TokenResponse:
    """
    Attributes:
        access_token (str): The JWT token
        expires_in (int): The number of seconds until the token expires. Typical lifetime is 60 minutes
        scope (list[Scope]): The scopes granted by the token, could be a subset of requested scopes
        token_type (Literal['bearer'] | Unset): The token type, always `bearer` Default: 'bearer'.
    """

    access_token: str
    expires_in: int
    scope: list[Scope]
    token_type: Literal["bearer"] | Unset = "bearer"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        expires_in = self.expires_in

        scope = []
        for scope_item_data in self.scope:
            scope_item = scope_item_data.value
            scope.append(scope_item)

        token_type = self.token_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_token": access_token,
                "expires_in": expires_in,
                "scope": scope,
            }
        )
        if token_type is not UNSET:
            field_dict["token_type"] = token_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token = d.pop("access_token")

        expires_in = d.pop("expires_in")

        scope = []
        _scope = d.pop("scope")
        for scope_item_data in _scope:
            scope_item = Scope(scope_item_data)

            scope.append(scope_item)

        token_type = cast(Literal["bearer"] | Unset, d.pop("token_type", UNSET))
        if token_type != "bearer" and not isinstance(token_type, Unset):
            raise ValueError(f"token_type must match const 'bearer', got '{token_type}'")

        token_response = cls(
            access_token=access_token,
            expires_in=expires_in,
            scope=scope,
            token_type=token_type,
        )

        token_response.additional_properties = d
        return token_response

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
