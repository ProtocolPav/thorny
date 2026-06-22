import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.quest_out import QuestOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    creator_thorny_ids: Union[None, Unset, list[int]] = UNSET,
    quest_types: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    active: Union[None, Unset, bool] = UNSET,
    future: Union[None, Unset, bool] = UNSET,
    past: Union[None, Unset, bool] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_creator_thorny_ids: Union[None, Unset, list[int]]
    if isinstance(creator_thorny_ids, Unset):
        json_creator_thorny_ids = UNSET
    elif isinstance(creator_thorny_ids, list):
        json_creator_thorny_ids = creator_thorny_ids

    else:
        json_creator_thorny_ids = creator_thorny_ids
    params["creator_thorny_ids"] = json_creator_thorny_ids

    json_quest_types: Union[None, Unset, list[str]]
    if isinstance(quest_types, Unset):
        json_quest_types = UNSET
    elif isinstance(quest_types, list):
        json_quest_types = quest_types

    else:
        json_quest_types = quest_types
    params["quest_types"] = json_quest_types

    json_time_start: Union[None, Unset, str]
    if isinstance(time_start, Unset):
        json_time_start = UNSET
    elif isinstance(time_start, datetime.datetime):
        json_time_start = time_start.isoformat()
    else:
        json_time_start = time_start
    params["time_start"] = json_time_start

    json_time_end: Union[None, Unset, str]
    if isinstance(time_end, Unset):
        json_time_end = UNSET
    elif isinstance(time_end, datetime.datetime):
        json_time_end = time_end.isoformat()
    else:
        json_time_end = time_end
    params["time_end"] = json_time_end

    json_active: Union[None, Unset, bool]
    if isinstance(active, Unset):
        json_active = UNSET
    else:
        json_active = active
    params["active"] = json_active

    json_future: Union[None, Unset, bool]
    if isinstance(future, Unset):
        json_future = UNSET
    else:
        json_future = future
    params["future"] = json_future

    json_past: Union[None, Unset, bool]
    if isinstance(past, Unset):
        json_past = UNSET
    else:
        json_past = past
    params["past"] = json_past

    json_page: Union[None, Unset, int]
    if isinstance(page, Unset):
        json_page = UNSET
    else:
        json_page = page
    params["page"] = json_page

    json_page_size: Union[None, Unset, int]
    if isinstance(page_size, Unset):
        json_page_size = UNSET
    else:
        json_page_size = page_size
    params["page_size"] = json_page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/quests_router",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["QuestOut"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = QuestOut.from_dict(response_200_item_data)

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, list["QuestOut"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    creator_thorny_ids: Union[None, Unset, list[int]] = UNSET,
    quest_types: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    active: Union[None, Unset, bool] = UNSET,
    future: Union[None, Unset, bool] = UNSET,
    past: Union[None, Unset, bool] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["QuestOut"]]]:
    """List Quests

     Get a list of Quests

    Args:
        creator_thorny_ids (Union[None, Unset, list[int]]): Filter by creator Thorny IDs
        quest_types (Union[None, Unset, list[str]]): Filter by quest type
        time_start (Union[None, Unset, datetime.datetime]): The start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): The end time to filter by
        active (Union[None, Unset, bool]): Filter by active quests_router
        future (Union[None, Unset, bool]): Filter by future quests_router
        past (Union[None, Unset, bool]): Filter by past quests_router
        page (Union[None, Unset, int]): The page to return. Default: 1 Default: 1.
        page_size (Union[None, Unset, int]): The size of each page in items. Default: 100 Default:
            100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['QuestOut']]]
    """

    kwargs = _get_kwargs(
        creator_thorny_ids=creator_thorny_ids,
        quest_types=quest_types,
        time_start=time_start,
        time_end=time_end,
        active=active,
        future=future,
        past=past,
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
    creator_thorny_ids: Union[None, Unset, list[int]] = UNSET,
    quest_types: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    active: Union[None, Unset, bool] = UNSET,
    future: Union[None, Unset, bool] = UNSET,
    past: Union[None, Unset, bool] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["QuestOut"]]]:
    """List Quests

     Get a list of Quests

    Args:
        creator_thorny_ids (Union[None, Unset, list[int]]): Filter by creator Thorny IDs
        quest_types (Union[None, Unset, list[str]]): Filter by quest type
        time_start (Union[None, Unset, datetime.datetime]): The start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): The end time to filter by
        active (Union[None, Unset, bool]): Filter by active quests_router
        future (Union[None, Unset, bool]): Filter by future quests_router
        past (Union[None, Unset, bool]): Filter by past quests_router
        page (Union[None, Unset, int]): The page to return. Default: 1 Default: 1.
        page_size (Union[None, Unset, int]): The size of each page in items. Default: 100 Default:
            100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['QuestOut']]
    """

    return sync_detailed(
        client=client,
        creator_thorny_ids=creator_thorny_ids,
        quest_types=quest_types,
        time_start=time_start,
        time_end=time_end,
        active=active,
        future=future,
        past=past,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    creator_thorny_ids: Union[None, Unset, list[int]] = UNSET,
    quest_types: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    active: Union[None, Unset, bool] = UNSET,
    future: Union[None, Unset, bool] = UNSET,
    past: Union[None, Unset, bool] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["QuestOut"]]]:
    """List Quests

     Get a list of Quests

    Args:
        creator_thorny_ids (Union[None, Unset, list[int]]): Filter by creator Thorny IDs
        quest_types (Union[None, Unset, list[str]]): Filter by quest type
        time_start (Union[None, Unset, datetime.datetime]): The start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): The end time to filter by
        active (Union[None, Unset, bool]): Filter by active quests_router
        future (Union[None, Unset, bool]): Filter by future quests_router
        past (Union[None, Unset, bool]): Filter by past quests_router
        page (Union[None, Unset, int]): The page to return. Default: 1 Default: 1.
        page_size (Union[None, Unset, int]): The size of each page in items. Default: 100 Default:
            100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['QuestOut']]]
    """

    kwargs = _get_kwargs(
        creator_thorny_ids=creator_thorny_ids,
        quest_types=quest_types,
        time_start=time_start,
        time_end=time_end,
        active=active,
        future=future,
        past=past,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    creator_thorny_ids: Union[None, Unset, list[int]] = UNSET,
    quest_types: Union[None, Unset, list[str]] = UNSET,
    time_start: Union[None, Unset, datetime.datetime] = UNSET,
    time_end: Union[None, Unset, datetime.datetime] = UNSET,
    active: Union[None, Unset, bool] = UNSET,
    future: Union[None, Unset, bool] = UNSET,
    past: Union[None, Unset, bool] = UNSET,
    page: Union[None, Unset, int] = 1,
    page_size: Union[None, Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["QuestOut"]]]:
    """List Quests

     Get a list of Quests

    Args:
        creator_thorny_ids (Union[None, Unset, list[int]]): Filter by creator Thorny IDs
        quest_types (Union[None, Unset, list[str]]): Filter by quest type
        time_start (Union[None, Unset, datetime.datetime]): The start time to filter by
        time_end (Union[None, Unset, datetime.datetime]): The end time to filter by
        active (Union[None, Unset, bool]): Filter by active quests_router
        future (Union[None, Unset, bool]): Filter by future quests_router
        past (Union[None, Unset, bool]): Filter by past quests_router
        page (Union[None, Unset, int]): The page to return. Default: 1 Default: 1.
        page_size (Union[None, Unset, int]): The size of each page in items. Default: 100 Default:
            100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['QuestOut']]
    """

    return (
        await asyncio_detailed(
            client=client,
            creator_thorny_ids=creator_thorny_ids,
            quest_types=quest_types,
            time_start=time_start,
            time_end=time_end,
            active=active,
            future=future,
            past=past,
            page=page,
            page_size=page_size,
        )
    ).parsed
