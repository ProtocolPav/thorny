from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user_out import UserOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    gamertag: Union[Unset, str] = UNSET,
    whitelist: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["gamertag"] = gamertag

    params["whitelist"] = whitelist

    params["discord_id"] = discord_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/guilds/me/users/lookup",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UserOut]]:
    if response.status_code == 200:
        response_200 = UserOut.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UserOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    gamertag: Union[Unset, str] = UNSET,
    whitelist: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, int] = UNSET,
) -> Response[Union[HTTPValidationError, UserOut]]:
    """Lookup User

     Looks up a guild member by gamertag, whitelisted gamertag, or Discord ID.
    Exactly one parameter must be provided.

    Args:
        gamertag (Union[Unset, str]):
        whitelist (Union[Unset, str]):
        discord_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserOut]]
    """

    kwargs = _get_kwargs(
        gamertag=gamertag,
        whitelist=whitelist,
        discord_id=discord_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    gamertag: Union[Unset, str] = UNSET,
    whitelist: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, int] = UNSET,
) -> Optional[Union[HTTPValidationError, UserOut]]:
    """Lookup User

     Looks up a guild member by gamertag, whitelisted gamertag, or Discord ID.
    Exactly one parameter must be provided.

    Args:
        gamertag (Union[Unset, str]):
        whitelist (Union[Unset, str]):
        discord_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserOut]
    """

    return sync_detailed(
        client=client,
        gamertag=gamertag,
        whitelist=whitelist,
        discord_id=discord_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    gamertag: Union[Unset, str] = UNSET,
    whitelist: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, int] = UNSET,
) -> Response[Union[HTTPValidationError, UserOut]]:
    """Lookup User

     Looks up a guild member by gamertag, whitelisted gamertag, or Discord ID.
    Exactly one parameter must be provided.

    Args:
        gamertag (Union[Unset, str]):
        whitelist (Union[Unset, str]):
        discord_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserOut]]
    """

    kwargs = _get_kwargs(
        gamertag=gamertag,
        whitelist=whitelist,
        discord_id=discord_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    gamertag: Union[Unset, str] = UNSET,
    whitelist: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, int] = UNSET,
) -> Optional[Union[HTTPValidationError, UserOut]]:
    """Lookup User

     Looks up a guild member by gamertag, whitelisted gamertag, or Discord ID.
    Exactly one parameter must be provided.

    Args:
        gamertag (Union[Unset, str]):
        whitelist (Union[Unset, str]):
        discord_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            gamertag=gamertag,
            whitelist=whitelist,
            discord_id=discord_id,
        )
    ).parsed
