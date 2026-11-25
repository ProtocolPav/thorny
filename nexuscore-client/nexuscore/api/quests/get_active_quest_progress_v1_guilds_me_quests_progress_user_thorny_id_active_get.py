from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.quest_progress_out import QuestProgressOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    thorny_id: int,
    *,
    quest_type: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_quest_type: None | str | Unset
    if isinstance(quest_type, Unset):
        json_quest_type = UNSET
    else:
        json_quest_type = quest_type
    params["quest_type"] = json_quest_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/quests/progress/user/{thorny_id}/active".format(
            thorny_id=quote(str(thorny_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | QuestProgressOut | None:
    if response.status_code == 200:
        response_200 = QuestProgressOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | QuestProgressOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
    quest_type: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | QuestProgressOut]:
    """Get Active Quest Progress

     Get User's Active Quest

    Returns the user's currently active quest.
    By default this is their regular (accepted) quest. Use `?quest_type=daily`
    to get their active daily quest instead.

    Args:
        thorny_id (int):
        quest_type (None | str | Unset): The quest type to look for, e.g. `daily`. When omitted,
            daily quests are excluded and the user's regular quest is used.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestProgressOut]
    """

    kwargs = _get_kwargs(
        thorny_id=thorny_id,
        quest_type=quest_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
    quest_type: None | str | Unset = UNSET,
) -> HTTPValidationError | QuestProgressOut | None:
    """Get Active Quest Progress

     Get User's Active Quest

    Returns the user's currently active quest.
    By default this is their regular (accepted) quest. Use `?quest_type=daily`
    to get their active daily quest instead.

    Args:
        thorny_id (int):
        quest_type (None | str | Unset): The quest type to look for, e.g. `daily`. When omitted,
            daily quests are excluded and the user's regular quest is used.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestProgressOut
    """

    return sync_detailed(
        thorny_id=thorny_id,
        client=client,
        quest_type=quest_type,
    ).parsed


async def asyncio_detailed(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
    quest_type: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | QuestProgressOut]:
    """Get Active Quest Progress

     Get User's Active Quest

    Returns the user's currently active quest.
    By default this is their regular (accepted) quest. Use `?quest_type=daily`
    to get their active daily quest instead.

    Args:
        thorny_id (int):
        quest_type (None | str | Unset): The quest type to look for, e.g. `daily`. When omitted,
            daily quests are excluded and the user's regular quest is used.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestProgressOut]
    """

    kwargs = _get_kwargs(
        thorny_id=thorny_id,
        quest_type=quest_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thorny_id: int,
    *,
    client: AuthenticatedClient,
    quest_type: None | str | Unset = UNSET,
) -> HTTPValidationError | QuestProgressOut | None:
    """Get Active Quest Progress

     Get User's Active Quest

    Returns the user's currently active quest.
    By default this is their regular (accepted) quest. Use `?quest_type=daily`
    to get their active daily quest instead.

    Args:
        thorny_id (int):
        quest_type (None | str | Unset): The quest type to look for, e.g. `daily`. When omitted,
            daily quests are excluded and the user's regular quest is used.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestProgressOut
    """

    return (
        await asyncio_detailed(
            thorny_id=thorny_id,
            client=client,
            quest_type=quest_type,
        )
    ).parsed
