from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.relay_model_type import RelayModelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RelayModel")


@_attrs_define
class RelayModel:
    """
    Attributes:
        type_ (RelayModelType): The type of relay Example: message.
        content (str): The content of the message Example: Hello, world!.
        embed_title (str): The title of the embed Example: Title.
        embed_content (str): The content of the embed Example: Hello, world!.
        name (Union[None, Unset, str]): The name to use for the webhook Example: ProtocolPav.
    """

    type_: RelayModelType
    content: str
    embed_title: str
    embed_content: str
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        content = self.content

        embed_title = self.embed_title

        embed_content = self.embed_content

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "content": content,
                "embed_title": embed_title,
                "embed_content": embed_content,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = RelayModelType(d.pop("type"))

        content = d.pop("content")

        embed_title = d.pop("embed_title")

        embed_content = d.pop("embed_content")

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        relay_model = cls(
            type_=type_,
            content=content,
            embed_title=embed_title,
            embed_content=embed_content,
            name=name,
        )

        relay_model.additional_properties = d
        return relay_model

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
