import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.quest_out import QuestOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    quest_date: datetime.date | None | Unset = UNSET,
    force: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_quest_date: None | str | Unset
    if isinstance(quest_date, Unset):
        json_quest_date = UNSET
    elif isinstance(quest_date, datetime.date):
        json_quest_date = quest_date.isoformat()
    else:
        json_quest_date = quest_date
    params["quest_date"] = json_quest_date

    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/guilds/me/quests/daily/generate",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | QuestOut | None:
    if response.status_code == 200:
        response_200 = QuestOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | QuestOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    quest_date: datetime.date | None | Unset = UNSET,
    force: bool | Unset = False,
) -> Response[HTTPValidationError | QuestOut]:
    """Generate Daily Quest

     Generate Daily Quest

    Daily quests are generated automatically, several days in advance. Use this to
    generate a day's quest immediately (today by default, or any future day), or with
    `force=true` to re-roll it.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.
        force (bool | Unset): Replace the day's daily quest if it already exists, including any
            admin edits. Players' unfinished progress on the old one is abandoned. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestOut]
    """

    kwargs = _get_kwargs(
        quest_date=quest_date,
        force=force,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    quest_date: datetime.date | None | Unset = UNSET,
    force: bool | Unset = False,
) -> HTTPValidationError | QuestOut | None:
    """Generate Daily Quest

     Generate Daily Quest

    Daily quests are generated automatically, several days in advance. Use this to
    generate a day's quest immediately (today by default, or any future day), or with
    `force=true` to re-roll it.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.
        force (bool | Unset): Replace the day's daily quest if it already exists, including any
            admin edits. Players' unfinished progress on the old one is abandoned. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestOut
    """

    return sync_detailed(
        client=client,
        quest_date=quest_date,
        force=force,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    quest_date: datetime.date | None | Unset = UNSET,
    force: bool | Unset = False,
) -> Response[HTTPValidationError | QuestOut]:
    """Generate Daily Quest

     Generate Daily Quest

    Daily quests are generated automatically, several days in advance. Use this to
    generate a day's quest immediately (today by default, or any future day), or with
    `force=true` to re-roll it.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.
        force (bool | Unset): Replace the day's daily quest if it already exists, including any
            admin edits. Players' unfinished progress on the old one is abandoned. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestOut]
    """

    kwargs = _get_kwargs(
        quest_date=quest_date,
        force=force,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    quest_date: datetime.date | None | Unset = UNSET,
    force: bool | Unset = False,
) -> HTTPValidationError | QuestOut | None:
    """Generate Daily Quest

     Generate Daily Quest

    Daily quests are generated automatically, several days in advance. Use this to
    generate a day's quest immediately (today by default, or any future day), or with
    `force=true` to re-roll it.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.
        force (bool | Unset): Replace the day's daily quest if it already exists, including any
            admin edits. Players' unfinished progress on the old one is abandoned. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestOut
    """

    return (
        await asyncio_detailed(
            client=client,
            quest_date=quest_date,
            force=force,
        )
    ).parsed
