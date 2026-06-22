from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GuildUpdate")


@_attrs_define
class GuildUpdate:
    """
    Attributes:
        name (Union[Unset, str]): The name of the guild
        currency_name (Union[Unset, str]): The guild's currency name (plural)
        currency_emoji (Union[Unset, str]): The emoji of the guild's currency
        level_up_message (Union[Unset, str]): Message sent when a user levels up
        join_message (Union[Unset, str]): Message sent when a user joins
        leave_message (Union[Unset, str]): Message sent when a user leaves
        xp_multiplier (Union[Unset, float]): XP multiplier for all guild members
        active (Union[Unset, bool]): Whether Thorny is in this guild
    """

    name: Union[Unset, str] = UNSET
    currency_name: Union[Unset, str] = UNSET
    currency_emoji: Union[Unset, str] = UNSET
    level_up_message: Union[Unset, str] = UNSET
    join_message: Union[Unset, str] = UNSET
    leave_message: Union[Unset, str] = UNSET
    xp_multiplier: Union[Unset, float] = UNSET
    active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        currency_name = self.currency_name

        currency_emoji = self.currency_emoji

        level_up_message = self.level_up_message

        join_message = self.join_message

        leave_message = self.leave_message

        xp_multiplier = self.xp_multiplier

        active = self.active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if currency_name is not UNSET:
            field_dict["currency_name"] = currency_name
        if currency_emoji is not UNSET:
            field_dict["currency_emoji"] = currency_emoji
        if level_up_message is not UNSET:
            field_dict["level_up_message"] = level_up_message
        if join_message is not UNSET:
            field_dict["join_message"] = join_message
        if leave_message is not UNSET:
            field_dict["leave_message"] = leave_message
        if xp_multiplier is not UNSET:
            field_dict["xp_multiplier"] = xp_multiplier
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        currency_name = d.pop("currency_name", UNSET)

        currency_emoji = d.pop("currency_emoji", UNSET)

        level_up_message = d.pop("level_up_message", UNSET)

        join_message = d.pop("join_message", UNSET)

        leave_message = d.pop("leave_message", UNSET)

        xp_multiplier = d.pop("xp_multiplier", UNSET)

        active = d.pop("active", UNSET)

        guild_update = cls(
            name=name,
            currency_name=currency_name,
            currency_emoji=currency_emoji,
            level_up_message=level_up_message,
            join_message=join_message,
            leave_message=leave_message,
            xp_multiplier=xp_multiplier,
            active=active,
        )

        guild_update.additional_properties = d
        return guild_update

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
