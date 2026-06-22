import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.profile_out import ProfileOut


T = TypeVar("T", bound="UserOut")


@_attrs_define
class UserOut:
    """
    Attributes:
        thorny_id (int): The ThornyID of a user. This is a unique number
        user_id (int): The Discord user ID.
        guild_id (int): The Discord guild ID this user is registered in.
        join_date (datetime.date): The date the ThornyID was created. Usually when a user joins the guild
        username (Union[None, str]):
        birthday (Union[None, datetime.date]):
        balance (int): The user's balance on the guild.
        active (bool): If the user is in the guild or not.
        role (Union[None, str]):
        patron (bool): Whether the user is a patron or not
        level (int): The user's level
        xp (int): The user's xp
        required_xp (int): The xp required to reach the next level
        last_message (Union[None, datetime.datetime]):
        gamertag (Union[None, str]):
        whitelist (Union[None, str]):
        xuid (Union[None, str]):
        location (Union[None, list[int]]):
        dimension (Union[None, str]):
        hidden (bool): Whether the user should be hidden on the Live Map
        profile (ProfileOut):
    """

    thorny_id: int
    user_id: int
    guild_id: int
    join_date: datetime.date
    username: Union[None, str]
    birthday: Union[None, datetime.date]
    balance: int
    active: bool
    role: Union[None, str]
    patron: bool
    level: int
    xp: int
    required_xp: int
    last_message: Union[None, datetime.datetime]
    gamertag: Union[None, str]
    whitelist: Union[None, str]
    xuid: Union[None, str]
    location: Union[None, list[int]]
    dimension: Union[None, str]
    hidden: bool
    profile: "ProfileOut"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thorny_id = self.thorny_id

        user_id = self.user_id

        guild_id = self.guild_id

        join_date = self.join_date.isoformat()

        username: Union[None, str]
        username = self.username

        birthday: Union[None, str]
        if isinstance(self.birthday, datetime.date):
            birthday = self.birthday.isoformat()
        else:
            birthday = self.birthday

        balance = self.balance

        active = self.active

        role: Union[None, str]
        role = self.role

        patron = self.patron

        level = self.level

        xp = self.xp

        required_xp = self.required_xp

        last_message: Union[None, str]
        if isinstance(self.last_message, datetime.datetime):
            last_message = self.last_message.isoformat()
        else:
            last_message = self.last_message

        gamertag: Union[None, str]
        gamertag = self.gamertag

        whitelist: Union[None, str]
        whitelist = self.whitelist

        xuid: Union[None, str]
        xuid = self.xuid

        location: Union[None, list[int]]
        if isinstance(self.location, list):
            location = []
            for location_type_0_item_data in self.location:
                location_type_0_item: int
                location_type_0_item = location_type_0_item_data
                location.append(location_type_0_item)

        else:
            location = self.location

        dimension: Union[None, str]
        dimension = self.dimension

        hidden = self.hidden

        profile = self.profile.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "thorny_id": thorny_id,
                "user_id": user_id,
                "guild_id": guild_id,
                "join_date": join_date,
                "username": username,
                "birthday": birthday,
                "balance": balance,
                "active": active,
                "role": role,
                "patron": patron,
                "level": level,
                "xp": xp,
                "required_xp": required_xp,
                "last_message": last_message,
                "gamertag": gamertag,
                "whitelist": whitelist,
                "xuid": xuid,
                "location": location,
                "dimension": dimension,
                "hidden": hidden,
                "profile": profile,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.profile_out import ProfileOut

        d = dict(src_dict)
        thorny_id = d.pop("thorny_id")

        user_id = d.pop("user_id")

        guild_id = d.pop("guild_id")

        join_date = isoparse(d.pop("join_date")).date()

        def _parse_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        username = _parse_username(d.pop("username"))

        def _parse_birthday(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birthday_type_0 = isoparse(data).date()

                return birthday_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        birthday = _parse_birthday(d.pop("birthday"))

        balance = d.pop("balance")

        active = d.pop("active")

        def _parse_role(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role = _parse_role(d.pop("role"))

        patron = d.pop("patron")

        level = d.pop("level")

        xp = d.pop("xp")

        required_xp = d.pop("required_xp")

        def _parse_last_message(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_message_type_0 = isoparse(data)

                return last_message_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_message = _parse_last_message(d.pop("last_message"))

        def _parse_gamertag(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        gamertag = _parse_gamertag(d.pop("gamertag"))

        def _parse_whitelist(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        whitelist = _parse_whitelist(d.pop("whitelist"))

        def _parse_xuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        xuid = _parse_xuid(d.pop("xuid"))

        def _parse_location(data: object) -> Union[None, list[int]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                location_type_0 = []
                _location_type_0 = data
                for location_type_0_item_data in _location_type_0:

                    def _parse_location_type_0_item(data: object) -> int:
                        return cast(int, data)

                    location_type_0_item = _parse_location_type_0_item(location_type_0_item_data)

                    location_type_0.append(location_type_0_item)

                return location_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[int]], data)

        location = _parse_location(d.pop("location"))

        def _parse_dimension(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        dimension = _parse_dimension(d.pop("dimension"))

        hidden = d.pop("hidden")

        profile = ProfileOut.from_dict(d.pop("profile"))

        user_out = cls(
            thorny_id=thorny_id,
            user_id=user_id,
            guild_id=guild_id,
            join_date=join_date,
            username=username,
            birthday=birthday,
            balance=balance,
            active=active,
            role=role,
            patron=patron,
            level=level,
            xp=xp,
            required_xp=required_xp,
            last_message=last_message,
            gamertag=gamertag,
            whitelist=whitelist,
            xuid=xuid,
            location=location,
            dimension=dimension,
            hidden=hidden,
            profile=profile,
        )

        user_out.additional_properties = d
        return user_out

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
