from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.guild_playtime_analysis import GuildPlaytimeAnalysis
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/playtime",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GuildPlaytimeAnalysis]:
    if response.status_code == 200:
        response_200 = GuildPlaytimeAnalysis.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GuildPlaytimeAnalysis]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GuildPlaytimeAnalysis]:
    """Get Guild Playtime

     This returns the guild's playtime summary. Playtime is in seconds.

    > [!warning]
    > The playtime analysis is currently a work in progress, and may not have all data.
    > Data shape might change in the future.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GuildPlaytimeAnalysis]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[GuildPlaytimeAnalysis]:
    """Get Guild Playtime

     This returns the guild's playtime summary. Playtime is in seconds.

    > [!warning]
    > The playtime analysis is currently a work in progress, and may not have all data.
    > Data shape might change in the future.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GuildPlaytimeAnalysis
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GuildPlaytimeAnalysis]:
    """Get Guild Playtime

     This returns the guild's playtime summary. Playtime is in seconds.

    > [!warning]
    > The playtime analysis is currently a work in progress, and may not have all data.
    > Data shape might change in the future.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GuildPlaytimeAnalysis]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[GuildPlaytimeAnalysis]:
    """Get Guild Playtime

     This returns the guild's playtime summary. Playtime is in seconds.

    > [!warning]
    > The playtime analysis is currently a work in progress, and may not have all data.
    > Data shape might change in the future.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GuildPlaytimeAnalysis
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
