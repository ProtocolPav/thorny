import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status_enum import StatusEnum

if TYPE_CHECKING:
    from ..models.user_out import UserOut


T = TypeVar("T", bound="ProjectOut")


@_attrs_define
class ProjectOut:
    """
    Attributes:
        project_id (str): The string ID of the project
        name (str): The name of the project
        thread_id (Union[None, int]):
        coordinates (list[int]): The coordinates of the project
        description (str): A short description of the project
        completed_on (Union[None, datetime.date]):
        pin_id (Union[None, int]):
        dimension (str): The dimension of the project
        started_on (Union[None, datetime.date]):
        status (StatusEnum):
        status_since (datetime.datetime): When the status was last updated
        owner (UserOut):
    """

    project_id: str
    name: str
    thread_id: Union[None, int]
    coordinates: list[int]
    description: str
    completed_on: Union[None, datetime.date]
    pin_id: Union[None, int]
    dimension: str
    started_on: Union[None, datetime.date]
    status: StatusEnum
    status_since: datetime.datetime
    owner: "UserOut"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        name = self.name

        thread_id: Union[None, int]
        thread_id = self.thread_id

        coordinates = self.coordinates

        description = self.description

        completed_on: Union[None, str]
        if isinstance(self.completed_on, datetime.date):
            completed_on = self.completed_on.isoformat()
        else:
            completed_on = self.completed_on

        pin_id: Union[None, int]
        pin_id = self.pin_id

        dimension = self.dimension

        started_on: Union[None, str]
        if isinstance(self.started_on, datetime.date):
            started_on = self.started_on.isoformat()
        else:
            started_on = self.started_on

        status = self.status.value

        status_since = self.status_since.isoformat()

        owner = self.owner.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "name": name,
                "thread_id": thread_id,
                "coordinates": coordinates,
                "description": description,
                "completed_on": completed_on,
                "pin_id": pin_id,
                "dimension": dimension,
                "started_on": started_on,
                "status": status,
                "status_since": status_since,
                "owner": owner,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_out import UserOut

        d = dict(src_dict)
        project_id = d.pop("project_id")

        name = d.pop("name")

        def _parse_thread_id(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        thread_id = _parse_thread_id(d.pop("thread_id"))

        coordinates = cast(list[int], d.pop("coordinates"))

        description = d.pop("description")

        def _parse_completed_on(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_on_type_0 = isoparse(data).date()

                return completed_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        completed_on = _parse_completed_on(d.pop("completed_on"))

        def _parse_pin_id(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        pin_id = _parse_pin_id(d.pop("pin_id"))

        dimension = d.pop("dimension")

        def _parse_started_on(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_on_type_0 = isoparse(data).date()

                return started_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        started_on = _parse_started_on(d.pop("started_on"))

        status = StatusEnum(d.pop("status"))

        status_since = isoparse(d.pop("status_since"))

        owner = UserOut.from_dict(d.pop("owner"))

        project_out = cls(
            project_id=project_id,
            name=name,
            thread_id=thread_id,
            coordinates=coordinates,
            description=description,
            completed_on=completed_on,
            pin_id=pin_id,
            dimension=dimension,
            started_on=started_on,
            status=status,
            status_since=status_since,
            owner=owner,
        )

        project_out.additional_properties = d
        return project_out

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
