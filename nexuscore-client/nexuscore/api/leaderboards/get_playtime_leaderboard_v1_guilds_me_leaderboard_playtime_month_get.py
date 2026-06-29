import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.leaderboard_model import LeaderboardModel
from ...types import Response


def _get_kwargs(
    month: datetime.date,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/leaderboard/playtime/{month}".format(
            month=quote(str(month), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | LeaderboardModel | None:
    if response.status_code == 200:
        response_200 = LeaderboardModel.from_dict(response.json())

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
) -> Response[HTTPValidationError | LeaderboardModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    month: datetime.date,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | LeaderboardModel]:
    """Get Playtime Leaderboard

     Returns the guild's playtime leaderboard, in order. Playtime is in seconds.

    Args:
        month (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LeaderboardModel]
    """

    kwargs = _get_kwargs(
        month=month,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    month: datetime.date,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | LeaderboardModel | None:
    """Get Playtime Leaderboard

     Returns the guild's playtime leaderboard, in order. Playtime is in seconds.

    Args:
        month (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LeaderboardModel
    """

    return sync_detailed(
        month=month,
        client=client,
    ).parsed


async def asyncio_detailed(
    month: datetime.date,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | LeaderboardModel]:
    """Get Playtime Leaderboard

     Returns the guild's playtime leaderboard, in order. Playtime is in seconds.

    Args:
        month (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LeaderboardModel]
    """

    kwargs = _get_kwargs(
        month=month,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    month: datetime.date,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | LeaderboardModel | None:
    """Get Playtime Leaderboard

     Returns the guild's playtime leaderboard, in order. Playtime is in seconds.

    Args:
        month (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LeaderboardModel
    """

    return (
        await asyncio_detailed(
            month=month,
            client=client,
        )
    ).parsed
