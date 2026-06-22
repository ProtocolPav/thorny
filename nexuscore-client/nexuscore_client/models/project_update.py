import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectUpdate")


@_attrs_define
class ProjectUpdate:
    """
    Attributes:
        name (Union[None, Unset, str]):
        thread_id (Union[None, Unset, int]):
        coordinates (Union[None, Unset, list[int]]):
        description (Union[None, Unset, str]):
        completed_on (Union[None, Unset, datetime.date]):
        pin_id (Union[None, Unset, int]):
        dimension (Union[None, Unset, str]):
        owner_id (Union[None, Unset, int]):
    """

    name: Union[None, Unset, str] = UNSET
    thread_id: Union[None, Unset, int] = UNSET
    coordinates: Union[None, Unset, list[int]] = UNSET
    description: Union[None, Unset, str] = UNSET
    completed_on: Union[None, Unset, datetime.date] = UNSET
    pin_id: Union[None, Unset, int] = UNSET
    dimension: Union[None, Unset, str] = UNSET
    owner_id: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        thread_id: Union[None, Unset, int]
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        coordinates: Union[None, Unset, list[int]]
        if isinstance(self.coordinates, Unset):
            coordinates = UNSET
        elif isinstance(self.coordinates, list):
            coordinates = self.coordinates

        else:
            coordinates = self.coordinates

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        completed_on: Union[None, Unset, str]
        if isinstance(self.completed_on, Unset):
            completed_on = UNSET
        elif isinstance(self.completed_on, datetime.date):
            completed_on = self.completed_on.isoformat()
        else:
            completed_on = self.completed_on

        pin_id: Union[None, Unset, int]
        if isinstance(self.pin_id, Unset):
            pin_id = UNSET
        else:
            pin_id = self.pin_id

        dimension: Union[None, Unset, str]
        if isinstance(self.dimension, Unset):
            dimension = UNSET
        else:
            dimension = self.dimension

        owner_id: Union[None, Unset, int]
        if isinstance(self.owner_id, Unset):
            owner_id = UNSET
        else:
            owner_id = self.owner_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates
        if description is not UNSET:
            field_dict["description"] = description
        if completed_on is not UNSET:
            field_dict["completed_on"] = completed_on
        if pin_id is not UNSET:
            field_dict["pin_id"] = pin_id
        if dimension is not UNSET:
            field_dict["dimension"] = dimension
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_thread_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        thread_id = _parse_thread_id(d.pop("thread_id", UNSET))

        def _parse_coordinates(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                coordinates_type_0 = cast(list[int], data)

                return coordinates_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        coordinates = _parse_coordinates(d.pop("coordinates", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_completed_on(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_on_type_0 = isoparse(data).date()

                return completed_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        completed_on = _parse_completed_on(d.pop("completed_on", UNSET))

        def _parse_pin_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        pin_id = _parse_pin_id(d.pop("pin_id", UNSET))

        def _parse_dimension(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dimension = _parse_dimension(d.pop("dimension", UNSET))

        def _parse_owner_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        owner_id = _parse_owner_id(d.pop("owner_id", UNSET))

        project_update = cls(
            name=name,
            thread_id=thread_id,
            coordinates=coordinates,
            description=description,
            completed_on=completed_on,
            pin_id=pin_id,
            dimension=dimension,
            owner_id=owner_id,
        )

        project_update.additional_properties = d
        return project_update

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
