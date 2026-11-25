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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/quests/daily",
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
) -> Response[HTTPValidationError | QuestOut]:
    """Get Daily Quest

     Get Daily Quest

    Returns the guild's daily quest for a UTC day, today by default.
    Daily quests reset at 00:00 UTC.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestOut]
    """

    kwargs = _get_kwargs(
        quest_date=quest_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    quest_date: datetime.date | None | Unset = UNSET,
) -> HTTPValidationError | QuestOut | None:
    """Get Daily Quest

     Get Daily Quest

    Returns the guild's daily quest for a UTC day, today by default.
    Daily quests reset at 00:00 UTC.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestOut
    """

    return sync_detailed(
        client=client,
        quest_date=quest_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    quest_date: datetime.date | None | Unset = UNSET,
) -> Response[HTTPValidationError | QuestOut]:
    """Get Daily Quest

     Get Daily Quest

    Returns the guild's daily quest for a UTC day, today by default.
    Daily quests reset at 00:00 UTC.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestOut]
    """

    kwargs = _get_kwargs(
        quest_date=quest_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    quest_date: datetime.date | None | Unset = UNSET,
) -> HTTPValidationError | QuestOut | None:
    """Get Daily Quest

     Get Daily Quest

    Returns the guild's daily quest for a UTC day, today by default.
    Daily quests reset at 00:00 UTC.

    Args:
        quest_date (datetime.date | None | Unset): The UTC date of the daily quest. Default:
            today.

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
        )
    ).parsed
