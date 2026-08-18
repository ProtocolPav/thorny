from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.quest_statistics_out import QuestStatisticsOut
from ...types import Response


def _get_kwargs(
    quest_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/quests/{quest_id}/statistics".format(
            quest_id=quote(str(quest_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | QuestStatisticsOut | None:
    if response.status_code == 200:
        response_200 = QuestStatisticsOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | QuestStatisticsOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    quest_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | QuestStatisticsOut]:
    """Get Quest Statistics

     Get Quest Statistics

    Returns aggregated statistics for a specific quest, including funnel data,
    completion timing, per-objective drop-off analysis, and daily activity.
    Useful for quest admins to analyse difficulty, engagement, and player behaviour.

    Args:
        quest_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestStatisticsOut]
    """

    kwargs = _get_kwargs(
        quest_id=quest_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    quest_id: int,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | QuestStatisticsOut | None:
    """Get Quest Statistics

     Get Quest Statistics

    Returns aggregated statistics for a specific quest, including funnel data,
    completion timing, per-objective drop-off analysis, and daily activity.
    Useful for quest admins to analyse difficulty, engagement, and player behaviour.

    Args:
        quest_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestStatisticsOut
    """

    return sync_detailed(
        quest_id=quest_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    quest_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | QuestStatisticsOut]:
    """Get Quest Statistics

     Get Quest Statistics

    Returns aggregated statistics for a specific quest, including funnel data,
    completion timing, per-objective drop-off analysis, and daily activity.
    Useful for quest admins to analyse difficulty, engagement, and player behaviour.

    Args:
        quest_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | QuestStatisticsOut]
    """

    kwargs = _get_kwargs(
        quest_id=quest_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    quest_id: int,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | QuestStatisticsOut | None:
    """Get Quest Statistics

     Get Quest Statistics

    Returns aggregated statistics for a specific quest, including funnel data,
    completion timing, per-objective drop-off analysis, and daily activity.
    Useful for quest admins to analyse difficulty, engagement, and player behaviour.

    Args:
        quest_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | QuestStatisticsOut
    """

    return (
        await asyncio_detailed(
            quest_id=quest_id,
            client=client,
        )
    ).parsed
