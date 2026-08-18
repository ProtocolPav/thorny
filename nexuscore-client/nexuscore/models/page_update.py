from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_in import ContentIn


T = TypeVar("T", bound="PageUpdate")


@_attrs_define
class PageUpdate:
    """
    Attributes:
        title (None | str | Unset):
        project_id (None | str | Unset):
        summary (None | str | Unset):
        category (None | str | Unset):
        tags (list[str] | None | Unset):
        cover_image (None | str | Unset):
        published (bool | None | Unset):
        locked (bool | None | Unset):
        content (ContentIn | None | Unset):
    """

    title: None | str | Unset = UNSET
    project_id: None | str | Unset = UNSET
    summary: None | str | Unset = UNSET
    category: None | str | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    cover_image: None | str | Unset = UNSET
    published: bool | None | Unset = UNSET
    locked: bool | None | Unset = UNSET
    content: ContentIn | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.content_in import ContentIn

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        summary: None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        cover_image: None | str | Unset
        if isinstance(self.cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = self.cover_image

        published: bool | None | Unset
        if isinstance(self.published, Unset):
            published = UNSET
        else:
            published = self.published

        locked: bool | None | Unset
        if isinstance(self.locked, Unset):
            locked = UNSET
        else:
            locked = self.locked

        content: dict[str, Any] | None | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, ContentIn):
            content = self.content.to_dict()
        else:
            content = self.content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if summary is not UNSET:
            field_dict["summary"] = summary
        if category is not UNSET:
            field_dict["category"] = category
        if tags is not UNSET:
            field_dict["tags"] = tags
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image
        if published is not UNSET:
            field_dict["published"] = published
        if locked is not UNSET:
            field_dict["locked"] = locked
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_in import ContentIn

        d = dict(src_dict)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_summary(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_category(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_cover_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cover_image = _parse_cover_image(d.pop("cover_image", UNSET))

        def _parse_published(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        published = _parse_published(d.pop("published", UNSET))

        def _parse_locked(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        locked = _parse_locked(d.pop("locked", UNSET))

        def _parse_content(data: object) -> ContentIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                content_type_0 = ContentIn.from_dict(data)

                return content_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContentIn | None | Unset, data)

        content = _parse_content(d.pop("content", UNSET))

        page_update = cls(
            title=title,
            project_id=project_id,
            summary=summary,
            category=category,
            tags=tags,
            cover_image=cover_image,
            published=published,
            locked=locked,
            content=content,
        )

        page_update.additional_properties = d
        return page_update

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
