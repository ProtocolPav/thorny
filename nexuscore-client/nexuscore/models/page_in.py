from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.content_in import ContentIn


T = TypeVar("T", bound="PageIn")


@_attrs_define
class PageIn:
    """
    Attributes:
        author_id (int): The ThornyID of the page author
        project_id (None | str):
        slug (str): The URL-safe slug ID of the page
        title (str): The title of the wiki page
        summary (None | str):
        category (str): The category this page belongs to
        tags (list[str]): Tags for categorizing the page
        cover_image (None | str):
        published (bool): Whether the page is publicly visible
        locked (bool): Whether the page is locked to prevent unauthorized edits
        content (ContentIn):
    """

    author_id: int
    project_id: None | str
    slug: str
    title: str
    summary: None | str
    category: str
    tags: list[str]
    cover_image: None | str
    published: bool
    locked: bool
    content: ContentIn
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        author_id = self.author_id

        project_id: None | str
        project_id = self.project_id

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

        content = self.content.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "author_id": author_id,
                "project_id": project_id,
                "slug": slug,
                "title": title,
                "summary": summary,
                "category": category,
                "tags": tags,
                "cover_image": cover_image,
                "published": published,
                "locked": locked,
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_in import ContentIn

        d = dict(src_dict)
        author_id = d.pop("author_id")

        def _parse_project_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        project_id = _parse_project_id(d.pop("project_id"))

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

        content = ContentIn.from_dict(d.pop("content"))

        page_in = cls(
            author_id=author_id,
            project_id=project_id,
            slug=slug,
            title=title,
            summary=summary,
            category=category,
            tags=tags,
            cover_image=cover_image,
            published=published,
            locked=locked,
            content=content,
        )

        page_in.additional_properties = d
        return page_in

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
