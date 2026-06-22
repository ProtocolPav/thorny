from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.channel_out import ChannelOut
    from ..models.feature_out import FeatureOut


T = TypeVar("T", bound="GuildOut")


@_attrs_define
class GuildOut:
    """
    Attributes:
        guild_id (int): The Discord guild ID
        name (str): The name of the guild
        currency_name (str): The guild's currency name (plural)
        currency_emoji (str): The emoji of the guild's currency
        level_up_message (str): Message sent when a user levels up
        join_message (str): Message sent when a user joins
        leave_message (str): Message sent when a user leaves
        xp_multiplier (float): XP multiplier for all guild members
        active (bool): Whether Thorny is in this guild
        channels (list['ChannelOut']):
        features (list['FeatureOut']):
    """

    guild_id: int
    name: str
    currency_name: str
    currency_emoji: str
    level_up_message: str
    join_message: str
    leave_message: str
    xp_multiplier: float
    active: bool
    channels: list["ChannelOut"]
    features: list["FeatureOut"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        guild_id = self.guild_id

        name = self.name

        currency_name = self.currency_name

        currency_emoji = self.currency_emoji

        level_up_message = self.level_up_message

        join_message = self.join_message

        leave_message = self.leave_message

        xp_multiplier = self.xp_multiplier

        active = self.active

        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.to_dict()
            channels.append(channels_item)

        features = []
        for features_item_data in self.features:
            features_item = features_item_data.to_dict()
            features.append(features_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "guild_id": guild_id,
                "name": name,
                "currency_name": currency_name,
                "currency_emoji": currency_emoji,
                "level_up_message": level_up_message,
                "join_message": join_message,
                "leave_message": leave_message,
                "xp_multiplier": xp_multiplier,
                "active": active,
                "channels": channels,
                "features": features,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.channel_out import ChannelOut
        from ..models.feature_out import FeatureOut

        d = dict(src_dict)
        guild_id = d.pop("guild_id")

        name = d.pop("name")

        currency_name = d.pop("currency_name")

        currency_emoji = d.pop("currency_emoji")

        level_up_message = d.pop("level_up_message")

        join_message = d.pop("join_message")

        leave_message = d.pop("leave_message")

        xp_multiplier = d.pop("xp_multiplier")

        active = d.pop("active")

        channels = []
        _channels = d.pop("channels")
        for channels_item_data in _channels:
            channels_item = ChannelOut.from_dict(channels_item_data)

            channels.append(channels_item)

        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = FeatureOut.from_dict(features_item_data)

            features.append(features_item)

        guild_out = cls(
            guild_id=guild_id,
            name=name,
            currency_name=currency_name,
            currency_emoji=currency_emoji,
            level_up_message=level_up_message,
            join_message=join_message,
            leave_message=leave_message,
            xp_multiplier=xp_multiplier,
            active=active,
            channels=channels,
            features=features,
        )

        guild_out.additional_properties = d
        return guild_out

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
