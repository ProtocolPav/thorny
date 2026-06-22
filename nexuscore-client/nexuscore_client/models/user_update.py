from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUpdate")


@_attrs_define
class UserUpdate:
    """
    Attributes:
        username (None | str | Unset):
        birthday (datetime.date | None | Unset):
        balance (int | None | Unset):
        active (bool | None | Unset):
        role (None | str | Unset):
        patron (bool | None | Unset):
        level (int | None | Unset):
        xp (int | None | Unset):
        required_xp (int | None | Unset):
        last_message (datetime.datetime | None | Unset):
        gamertag (None | str | Unset):
        whitelist (None | str | Unset):
        location (list[int] | None | Unset):
        dimension (None | str | Unset):
        hidden (bool | None | Unset):
        xuid (None | str | Unset):
    """

    username: None | str | Unset = UNSET
    birthday: datetime.date | None | Unset = UNSET
    balance: int | None | Unset = UNSET
    active: bool | None | Unset = UNSET
    role: None | str | Unset = UNSET
    patron: bool | None | Unset = UNSET
    level: int | None | Unset = UNSET
    xp: int | None | Unset = UNSET
    required_xp: int | None | Unset = UNSET
    last_message: datetime.datetime | None | Unset = UNSET
    gamertag: None | str | Unset = UNSET
    whitelist: None | str | Unset = UNSET
    location: list[int] | None | Unset = UNSET
    dimension: None | str | Unset = UNSET
    hidden: bool | None | Unset = UNSET
    xuid: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username: None | str | Unset
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        birthday: None | str | Unset
        if isinstance(self.birthday, Unset):
            birthday = UNSET
        elif isinstance(self.birthday, datetime.date):
            birthday = self.birthday.isoformat()
        else:
            birthday = self.birthday

        balance: int | None | Unset
        if isinstance(self.balance, Unset):
            balance = UNSET
        else:
            balance = self.balance

        active: bool | None | Unset
        if isinstance(self.active, Unset):
            active = UNSET
        else:
            active = self.active

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        patron: bool | None | Unset
        if isinstance(self.patron, Unset):
            patron = UNSET
        else:
            patron = self.patron

        level: int | None | Unset
        if isinstance(self.level, Unset):
            level = UNSET
        else:
            level = self.level

        xp: int | None | Unset
        if isinstance(self.xp, Unset):
            xp = UNSET
        else:
            xp = self.xp

        required_xp: int | None | Unset
        if isinstance(self.required_xp, Unset):
            required_xp = UNSET
        else:
            required_xp = self.required_xp

        last_message: None | str | Unset
        if isinstance(self.last_message, Unset):
            last_message = UNSET
        elif isinstance(self.last_message, datetime.datetime):
            last_message = self.last_message.isoformat()
        else:
            last_message = self.last_message

        gamertag: None | str | Unset
        if isinstance(self.gamertag, Unset):
            gamertag = UNSET
        else:
            gamertag = self.gamertag

        whitelist: None | str | Unset
        if isinstance(self.whitelist, Unset):
            whitelist = UNSET
        else:
            whitelist = self.whitelist

        location: list[int] | None | Unset
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

        dimension: None | str | Unset
        if isinstance(self.dimension, Unset):
            dimension = UNSET
        else:
            dimension = self.dimension

        hidden: bool | None | Unset
        if isinstance(self.hidden, Unset):
            hidden = UNSET
        else:
            hidden = self.hidden

        xuid: None | str | Unset
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

        def _parse_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        username = _parse_username(d.pop("username", UNSET))

        def _parse_birthday(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birthday_type_0 = datetime.date.fromisoformat(data)

                return birthday_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        birthday = _parse_birthday(d.pop("birthday", UNSET))

        def _parse_balance(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        balance = _parse_balance(d.pop("balance", UNSET))

        def _parse_active(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        active = _parse_active(d.pop("active", UNSET))

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_patron(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        patron = _parse_patron(d.pop("patron", UNSET))

        def _parse_level(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        level = _parse_level(d.pop("level", UNSET))

        def _parse_xp(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        xp = _parse_xp(d.pop("xp", UNSET))

        def _parse_required_xp(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        required_xp = _parse_required_xp(d.pop("required_xp", UNSET))

        def _parse_last_message(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_message_type_0 = datetime.datetime.fromisoformat(data)

                return last_message_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_message = _parse_last_message(d.pop("last_message", UNSET))

        def _parse_gamertag(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        gamertag = _parse_gamertag(d.pop("gamertag", UNSET))

        def _parse_whitelist(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        whitelist = _parse_whitelist(d.pop("whitelist", UNSET))

        def _parse_location(data: object) -> list[int] | None | Unset:
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
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[int] | None | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_dimension(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dimension = _parse_dimension(d.pop("dimension", UNSET))

        def _parse_hidden(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        hidden = _parse_hidden(d.pop("hidden", UNSET))

        def _parse_xuid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

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
