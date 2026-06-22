from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ChannelOut")


@_attrs_define
class ChannelOut:
    """
    Attributes:
        channel_type (str): The type of channel
        channel_id (int): The channel ID
    """

    channel_type: str
    channel_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel_type = self.channel_type

        channel_id = self.channel_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_type": channel_type,
                "channel_id": channel_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel_type = d.pop("channel_type")

        channel_id = d.pop("channel_id")

        channel_out = cls(
            channel_type=channel_type,
            channel_id=channel_id,
        )

        channel_out.additional_properties = d
        return channel_out

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
