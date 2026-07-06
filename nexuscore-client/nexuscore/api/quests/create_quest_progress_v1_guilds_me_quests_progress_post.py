from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.quest_progress_in import QuestProgressIn
from ...models.quest_progress_out import QuestProgressOut
from ...types import Response


def _get_kwargs(
    *,
    body: QuestProgressIn,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/guilds/me/quests/progress",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | QuestProgressOut | None:
    if response.status_code == 201:
        response_201 = QuestProgressOut.from_dict(response.json())

        return response_201

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
    *,
    client: AuthenticatedClient,
    body: QuestProgressIn,
) -> Response[HTTPValidationError | QuestProgressOut]:
    r"""Create Quest Progress

     Create New Quest Progress

    Adds a new quest to a user, tracking their progress.
    Automatically sets the quest progress to \"active\".

    Args:
        body (QuestProgressIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestProgressOut]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: QuestProgressIn,
) -> HTTPValidationError | QuestProgressOut | None:
    r"""Create Quest Progress

     Create New Quest Progress

    Adds a new quest to a user, tracking their progress.
    Automatically sets the quest progress to \"active\".

    Args:
        body (QuestProgressIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestProgressOut
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: QuestProgressIn,
) -> Response[HTTPValidationError | QuestProgressOut]:
    r"""Create Quest Progress

     Create New Quest Progress

    Adds a new quest to a user, tracking their progress.
    Automatically sets the quest progress to \"active\".

    Args:
        body (QuestProgressIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestProgressOut]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: QuestProgressIn,
) -> HTTPValidationError | QuestProgressOut | None:
    r"""Create Quest Progress

     Create New Quest Progress

    Adds a new quest to a user, tracking their progress.
    Automatically sets the quest progress to \"active\".

    Args:
        body (QuestProgressIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestProgressOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
