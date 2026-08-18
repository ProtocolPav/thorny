from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_out import ContentOut
    from ..models.project_out import ProjectOut
    from ..models.user_out import UserOut


T = TypeVar("T", bound="PageOut")


@_attrs_define
class PageOut:
    """
    Attributes:
        slug (str): The URL-safe slug ID of the page
        title (str): The title of the wiki page
        summary (None | str):
        category (str): The category this page belongs to
        tags (list[str]): Tags for categorizing the page
        cover_image (None | str):
        published (bool): Whether the page is publicly visible
        locked (bool): Whether the page is locked to prevent unauthorized edits
        view_count (int): The number of times this page has been viewed
        created_at (datetime.datetime): When the page was created
        updated_at (datetime.datetime): When the page was last updated
        author (UserOut):
        content (ContentOut):
        project (None | ProjectOut | Unset):
    """

    slug: str
    title: str
    summary: None | str
    category: str
    tags: list[str]
    cover_image: None | str
    published: bool
    locked: bool
    view_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author: UserOut
    content: ContentOut
    project: None | ProjectOut | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_out import ProjectOut

        slug = self.slug

        title = self.title

        summary: None | str
        summary = self.summary

        category = self.category

        tags = self.tags

        cover_image: None | str
        cover_image = self.cover_image

        published = self.published

        locked = self.locked

        view_count = self.view_count

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        author = self.author.to_dict()

        content = self.content.to_dict()

        project: dict[str, Any] | None | Unset
        if isinstance(self.project, Unset):
            project = UNSET
        elif isinstance(self.project, ProjectOut):
            project = self.project.to_dict()
        else:
            project = self.project

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "slug": slug,
                "title": title,
                "summary": summary,
                "category": category,
                "tags": tags,
                "cover_image": cover_image,
                "published": published,
                "locked": locked,
                "view_count": view_count,
                "created_at": created_at,
                "updated_at": updated_at,
                "author": author,
                "content": content,
            }
        )
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_out import ContentOut
        from ..models.project_out import ProjectOut
        from ..models.user_out import UserOut

        d = dict(src_dict)
        slug = d.pop("slug")

        title = d.pop("title")

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        category = d.pop("category")

        tags = cast(list[str], d.pop("tags"))

        def _parse_cover_image(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cover_image = _parse_cover_image(d.pop("cover_image"))

        published = d.pop("published")

        locked = d.pop("locked")

        view_count = d.pop("view_count")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        author = UserOut.from_dict(d.pop("author"))

        content = ContentOut.from_dict(d.pop("content"))

        def _parse_project(data: object) -> None | ProjectOut | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                project_type_0 = ProjectOut.from_dict(data)

                return project_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectOut | Unset, data)

        project = _parse_project(d.pop("project", UNSET))

        page_out = cls(
            slug=slug,
            title=title,
            summary=summary,
            category=category,
            tags=tags,
            cover_image=cover_image,
            published=published,
            locked=locked,
            view_count=view_count,
            created_at=created_at,
            updated_at=updated_at,
            author=author,
            content=content,
            project=project,
        )

        page_out.additional_properties = d
        return page_out

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
