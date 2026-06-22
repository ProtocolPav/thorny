import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUpdate")


@_attrs_define
class UserUpdate:
    """
    Attributes:
        username (Union[None, Unset, str]):
        birthday (Union[None, Unset, datetime.date]):
        balance (Union[None, Unset, int]):
        active (Union[None, Unset, bool]):
        role (Union[None, Unset, str]):
        patron (Union[None, Unset, bool]):
        level (Union[None, Unset, int]):
        xp (Union[None, Unset, int]):
        required_xp (Union[None, Unset, int]):
        last_message (Union[None, Unset, datetime.datetime]):
        gamertag (Union[None, Unset, str]):
        whitelist (Union[None, Unset, str]):
        location (Union[None, Unset, list[int]]):
        dimension (Union[None, Unset, str]):
        hidden (Union[None, Unset, bool]):
        xuid (Union[None, Unset, str]):
    """

    username: Union[None, Unset, str] = UNSET
    birthday: Union[None, Unset, datetime.date] = UNSET
    balance: Union[None, Unset, int] = UNSET
    active: Union[None, Unset, bool] = UNSET
    role: Union[None, Unset, str] = UNSET
    patron: Union[None, Unset, bool] = UNSET
    level: Union[None, Unset, int] = UNSET
    xp: Union[None, Unset, int] = UNSET
    required_xp: Union[None, Unset, int] = UNSET
    last_message: Union[None, Unset, datetime.datetime] = UNSET
    gamertag: Union[None, Unset, str] = UNSET
    whitelist: Union[None, Unset, str] = UNSET
    location: Union[None, Unset, list[int]] = UNSET
    dimension: Union[None, Unset, str] = UNSET
    hidden: Union[None, Unset, bool] = UNSET
    xuid: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        birthday: Union[None, Unset, str]
        if isinstance(self.birthday, Unset):
            birthday = UNSET
        elif isinstance(self.birthday, datetime.date):
            birthday = self.birthday.isoformat()
        else:
            birthday = self.birthday

        balance: Union[None, Unset, int]
        if isinstance(self.balance, Unset):
            balance = UNSET
        else:
            balance = self.balance

        active: Union[None, Unset, bool]
        if isinstance(self.active, Unset):
            active = UNSET
        else:
            active = self.active

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        patron: Union[None, Unset, bool]
        if isinstance(self.patron, Unset):
            patron = UNSET
        else:
            patron = self.patron

        level: Union[None, Unset, int]
        if isinstance(self.level, Unset):
            level = UNSET
        else:
            level = self.level

        xp: Union[None, Unset, int]
        if isinstance(self.xp, Unset):
            xp = UNSET
        else:
            xp = self.xp

        required_xp: Union[None, Unset, int]
        if isinstance(self.required_xp, Unset):
            required_xp = UNSET
        else:
            required_xp = self.required_xp

        last_message: Union[None, Unset, str]
        if isinstance(self.last_message, Unset):
            last_message = UNSET
        elif isinstance(self.last_message, datetime.datetime):
            last_message = self.last_message.isoformat()
        else:
            last_message = self.last_message

        gamertag: Union[None, Unset, str]
        if isinstance(self.gamertag, Unset):
            gamertag = UNSET
        else:
            gamertag = self.gamertag

        whitelist: Union[None, Unset, str]
        if isinstance(self.whitelist, Unset):
            whitelist = UNSET
        else:
            whitelist = self.whitelist

        location: Union[None, Unset, list[int]]
        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, list):
            location = []
            for location_type_0_item_data in self.location:
                location_type_0_item: int
                location_type_0_item = location_type_0_item_data
                location.append(location_type_0_item)

        else:
            location = self.location

        dimension: Union[None, Unset, str]
        if isinstance(self.dimension, Unset):
            dimension = UNSET
        else:
            dimension = self.dimension

        hidden: Union[None, Unset, bool]
        if isinstance(self.hidden, Unset):
            hidden = UNSET
        else:
            hidden = self.hidden

        xuid: Union[None, Unset, str]
        if isinstance(self.xuid, Unset):
            xuid = UNSET
        else:
            xuid = self.xuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if birthday is not UNSET:
            field_dict["birthday"] = birthday
        if balance is not UNSET:
            field_dict["balance"] = balance
        if active is not UNSET:
            field_dict["active"] = active
        if role is not UNSET:
            field_dict["role"] = role
        if patron is not UNSET:
            field_dict["patron"] = patron
        if level is not UNSET:
            field_dict["level"] = level
        if xp is not UNSET:
            field_dict["xp"] = xp
        if required_xp is not UNSET:
            field_dict["required_xp"] = required_xp
        if last_message is not UNSET:
            field_dict["last_message"] = last_message
        if gamertag is not UNSET:
            field_dict["gamertag"] = gamertag
        if whitelist is not UNSET:
            field_dict["whitelist"] = whitelist
        if location is not UNSET:
            field_dict["location"] = location
        if dimension is not UNSET:
            field_dict["dimension"] = dimension
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if xuid is not UNSET:
            field_dict["xuid"] = xuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        def _parse_birthday(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birthday_type_0 = isoparse(data).date()

                return birthday_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        birthday = _parse_birthday(d.pop("birthday", UNSET))

        def _parse_balance(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        balance = _parse_balance(d.pop("balance", UNSET))

        def _parse_active(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        active = _parse_active(d.pop("active", UNSET))

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_patron(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        patron = _parse_patron(d.pop("patron", UNSET))

        def _parse_level(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        level = _parse_level(d.pop("level", UNSET))

        def _parse_xp(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        xp = _parse_xp(d.pop("xp", UNSET))

        def _parse_required_xp(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        required_xp = _parse_required_xp(d.pop("required_xp", UNSET))

        def _parse_last_message(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_message_type_0 = isoparse(data)

                return last_message_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_message = _parse_last_message(d.pop("last_message", UNSET))

        def _parse_gamertag(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gamertag = _parse_gamertag(d.pop("gamertag", UNSET))

        def _parse_whitelist(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        whitelist = _parse_whitelist(d.pop("whitelist", UNSET))

        def _parse_location(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
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
            return cast(Union[None, Unset, list[int]], data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_dimension(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dimension = _parse_dimension(d.pop("dimension", UNSET))

        def _parse_hidden(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        hidden = _parse_hidden(d.pop("hidden", UNSET))

        def _parse_xuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        xuid = _parse_xuid(d.pop("xuid", UNSET))

        user_update = cls(
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
            location=location,
            dimension=dimension,
            hidden=hidden,
            xuid=xuid,
        )

        user_update.additional_properties = d
        return user_update

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
