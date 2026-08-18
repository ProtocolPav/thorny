from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_out_data_item import ContentOutDataItem
    from ..models.user_out import UserOut


T = TypeVar("T", bound="ContentOut")


@_attrs_define
class ContentOut:
    """
    Attributes:
        version (int): The version number, scoped per page
        edited_by (UserOut):
        change_note (str): A note describing what changed in this version
        data (list[ContentOutDataItem]): The full React editor document as an opaque JSON object
        editor_type (str | Unset): The editor type used to create this content Default: 'blocknote'.
    """

    version: int
    edited_by: UserOut
    change_note: str
    data: list[ContentOutDataItem]
    editor_type: str | Unset = "blocknote"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        edited_by = self.edited_by.to_dict()

        change_note = self.change_note

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        editor_type = self.editor_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "edited_by": edited_by,
                "change_note": change_note,
                "data": data,
            }
        )
        if editor_type is not UNSET:
            field_dict["editor_type"] = editor_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_out_data_item import ContentOutDataItem
        from ..models.user_out import UserOut

        d = dict(src_dict)
        version = d.pop("version")

        edited_by = UserOut.from_dict(d.pop("edited_by"))

        change_note = d.pop("change_note")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ContentOutDataItem.from_dict(data_item_data)

            data.append(data_item)

        editor_type = d.pop("editor_type", UNSET)

        content_out = cls(
            version=version,
            edited_by=edited_by,
            change_note=change_note,
            data=data,
            editor_type=editor_type,
        )

        content_out.additional_properties = d
        return content_out

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
