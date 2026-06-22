import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="OnlineMember")


@_attrs_define
class OnlineMember:
    """
    Attributes:
        thorny_id (int): The ThornyID of the user
        user_id (int): The Discord ID of the user
        session (datetime.datetime): The date and time when the session started
        username (str): The username of the user
        whitelist (str): The gamertag of the user
        location (list[int]): The last in-game location of the user
        dimension (str): The last in-game dimension the user was in
        hidden (bool): Whether the user should be hidden on the Live Map
        xuid (Union[None, str]):
    """

    thorny_id: int
    user_id: int
    session: datetime.datetime
    username: str
    whitelist: str
    location: list[int]
    dimension: str
    hidden: bool
    xuid: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thorny_id = self.thorny_id

        user_id = self.user_id

        session = self.session.isoformat()

        username = self.username

        whitelist = self.whitelist

        location = []
        for location_item_data in self.location:
            location_item: int
            location_item = location_item_data
            location.append(location_item)

        dimension = self.dimension

        hidden = self.hidden

        xuid: Union[None, str]
        xuid = self.xuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thorny_id": thorny_id,
                "user_id": user_id,
                "session": session,
                "username": username,
                "whitelist": whitelist,
                "location": location,
                "dimension": dimension,
                "hidden": hidden,
                "xuid": xuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        thorny_id = d.pop("thorny_id")

        user_id = d.pop("user_id")

        session = isoparse(d.pop("session"))

        username = d.pop("username")

        whitelist = d.pop("whitelist")

        location = []
        _location = d.pop("location")
        for location_item_data in _location:

            def _parse_location_item(data: object) -> int:
                return cast(int, data)

            location_item = _parse_location_item(location_item_data)

            location.append(location_item)

        dimension = d.pop("dimension")

        hidden = d.pop("hidden")

        def _parse_xuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        xuid = _parse_xuid(d.pop("xuid"))

        online_member = cls(
            thorny_id=thorny_id,
            user_id=user_id,
            session=session,
            username=username,
            whitelist=whitelist,
            location=location,
            dimension=dimension,
            hidden=hidden,
            xuid=xuid,
        )

        online_member.additional_properties = d
        return online_member

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
