from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_wiki_pages_v1_guilds_me_wiki_get_sort_by_type_0 import ListWikiPagesV1GuildsMeWikiGetSortByType0
from ...models.list_wiki_pages_v1_guilds_me_wiki_get_sort_order_type_0 import (
    ListWikiPagesV1GuildsMeWikiGetSortOrderType0,
)
from ...models.page_out import PageOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    published: bool | None | Unset = UNSET,
    category: None | str | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    search: None | str | Unset = UNSET,
    sort_by: ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset = UNSET,
    sort_order: ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset = UNSET,
    page: int | None | Unset = 1,
    page_size: int | None | Unset = 10,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_published: bool | None | Unset
    if isinstance(published, Unset):
        json_published = UNSET
    else:
        json_published = published
    params["published"] = json_published

    json_category: None | str | Unset
    if isinstance(category, Unset):
        json_category = UNSET
    else:
        json_category = category
    params["category"] = json_category

    json_tags: list[str] | None | Unset
    if isinstance(tags, Unset):
        json_tags = UNSET
    elif isinstance(tags, list):
        json_tags = tags

    else:
        json_tags = tags
    params["tags"] = json_tags

    json_search: None | str | Unset
    if isinstance(search, Unset):
        json_search = UNSET
    else:
        json_search = search
    params["search"] = json_search

    json_sort_by: None | str | Unset
    if isinstance(sort_by, Unset):
        json_sort_by = UNSET
    elif isinstance(sort_by, ListWikiPagesV1GuildsMeWikiGetSortByType0):
        json_sort_by = sort_by.value
    else:
        json_sort_by = sort_by
    params["sort_by"] = json_sort_by

    json_sort_order: None | str | Unset
    if isinstance(sort_order, Unset):
        json_sort_order = UNSET
    elif isinstance(sort_order, ListWikiPagesV1GuildsMeWikiGetSortOrderType0):
        json_sort_order = sort_order.value
    else:
        json_sort_order = sort_order
    params["sort_order"] = json_sort_order

    json_page: int | None | Unset
    if isinstance(page, Unset):
        json_page = UNSET
    else:
        json_page = page
    params["page"] = json_page

    json_page_size: int | None | Unset
    if isinstance(page_size, Unset):
        json_page_size = UNSET
    else:
        json_page_size = page_size
    params["page_size"] = json_page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/wiki",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[PageOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PageOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | list[PageOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    published: bool | None | Unset = UNSET,
    category: None | str | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    search: None | str | Unset = UNSET,
    sort_by: ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset = UNSET,
    sort_order: ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset = UNSET,
    page: int | None | Unset = 1,
    page_size: int | None | Unset = 10,
) -> Response[HTTPValidationError | list[PageOut]]:
    """List Wiki Pages

     Get a list of Wiki Pages

    Args:
        published (bool | None | Unset): Filter by published status
        category (None | str | Unset): Filter by category
        tags (list[str] | None | Unset): Filter by tags
        search (None | str | Unset): Fuzzy search by page title (summary and content comes later)
        sort_by (ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset): Sort by field
        sort_order (ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset): Sort order
        page (int | None | Unset): The page number to return Default: 1.
        page_size (int | None | Unset): The number of items per page Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[PageOut]]
    """

    kwargs = _get_kwargs(
        published=published,
        category=category,
        tags=tags,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    published: bool | None | Unset = UNSET,
    category: None | str | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    search: None | str | Unset = UNSET,
    sort_by: ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset = UNSET,
    sort_order: ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset = UNSET,
    page: int | None | Unset = 1,
    page_size: int | None | Unset = 10,
) -> HTTPValidationError | list[PageOut] | None:
    """List Wiki Pages

     Get a list of Wiki Pages

    Args:
        published (bool | None | Unset): Filter by published status
        category (None | str | Unset): Filter by category
        tags (list[str] | None | Unset): Filter by tags
        search (None | str | Unset): Fuzzy search by page title (summary and content comes later)
        sort_by (ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset): Sort by field
        sort_order (ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset): Sort order
        page (int | None | Unset): The page number to return Default: 1.
        page_size (int | None | Unset): The number of items per page Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[PageOut]
    """

    return sync_detailed(
        client=client,
        published=published,
        category=category,
        tags=tags,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    published: bool | None | Unset = UNSET,
    category: None | str | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    search: None | str | Unset = UNSET,
    sort_by: ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset = UNSET,
    sort_order: ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset = UNSET,
    page: int | None | Unset = 1,
    page_size: int | None | Unset = 10,
) -> Response[HTTPValidationError | list[PageOut]]:
    """List Wiki Pages

     Get a list of Wiki Pages

    Args:
        published (bool | None | Unset): Filter by published status
        category (None | str | Unset): Filter by category
        tags (list[str] | None | Unset): Filter by tags
        search (None | str | Unset): Fuzzy search by page title (summary and content comes later)
        sort_by (ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset): Sort by field
        sort_order (ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset): Sort order
        page (int | None | Unset): The page number to return Default: 1.
        page_size (int | None | Unset): The number of items per page Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[PageOut]]
    """

    kwargs = _get_kwargs(
        published=published,
        category=category,
        tags=tags,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    published: bool | None | Unset = UNSET,
    category: None | str | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    search: None | str | Unset = UNSET,
    sort_by: ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset = UNSET,
    sort_order: ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset = UNSET,
    page: int | None | Unset = 1,
    page_size: int | None | Unset = 10,
) -> HTTPValidationError | list[PageOut] | None:
    """List Wiki Pages

     Get a list of Wiki Pages

    Args:
        published (bool | None | Unset): Filter by published status
        category (None | str | Unset): Filter by category
        tags (list[str] | None | Unset): Filter by tags
        search (None | str | Unset): Fuzzy search by page title (summary and content comes later)
        sort_by (ListWikiPagesV1GuildsMeWikiGetSortByType0 | None | Unset): Sort by field
        sort_order (ListWikiPagesV1GuildsMeWikiGetSortOrderType0 | None | Unset): Sort order
        page (int | None | Unset): The page number to return Default: 1.
        page_size (int | None | Unset): The number of items per page Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[PageOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            published=published,
            category=category,
            tags=tags,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size,
        )
    ).parsed
