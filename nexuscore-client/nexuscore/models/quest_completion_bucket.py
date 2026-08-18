from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="QuestCompletionBucket")


@_attrs_define
class QuestCompletionBucket:
    """
    Attributes:
        bucket_start_seconds (int): Start of the time bucket in seconds
        bucket_end_seconds (int): End of the time bucket in seconds
        count (int): Number of completions that fall within this bucket
    """

    bucket_start_seconds: int
    bucket_end_seconds: int
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket_start_seconds = self.bucket_start_seconds

        bucket_end_seconds = self.bucket_end_seconds

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket_start_seconds": bucket_start_seconds,
                "bucket_end_seconds": bucket_end_seconds,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bucket_start_seconds = d.pop("bucket_start_seconds")

        bucket_end_seconds = d.pop("bucket_end_seconds")

        count = d.pop("count")

        quest_completion_bucket = cls(
            bucket_start_seconds=bucket_start_seconds,
            bucket_end_seconds=bucket_end_seconds,
            count=count,
        )

        quest_completion_bucket.additional_properties = d
        return quest_completion_bucket

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
